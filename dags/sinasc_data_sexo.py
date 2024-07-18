from airflow import DAG
from airflow.operators.python_operator import PythonOperator, BranchPythonOperator
from airflow.operators.mysql_operator import MySqlOperator
from airflow.operators.dummy_operator import DummyOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

"""
Extrator web_crawler_sinasc

https://github.com/Foradocubo/web_crawler_sinasc 

"""

def extract_and_load_data():
    import pandas as pd
    import mysql.connector
    from bs4 import BeautifulSoup
    from time import sleep
    from datetime import datetime
    from selenium import webdriver
    from selenium.webdriver.chrome.service import Service
    from selenium.common.exceptions import NoSuchElementException
    from webdriver_manager.chrome import ChromeDriverManager

    def setup_driver():
        """Configura e retorna o driver do Chrome."""
        service = Service(ChromeDriverManager().install())
        return webdriver.Chrome(service=service)

    def get_current_month_option():
        """Retorna a opção do mês atual para seleção."""
        current_month = int(datetime.now().strftime("%m"))
        return current_month if current_month != 1 else 13

    def extract_data(driver):
        """Extrai dados do site e retorna o HTML."""
        driver.get('http://tabnet.saude.prefeitura.sp.gov.br/cgi/tabcgi.exe?secretarias/saude/TABNET/sinasc/nascido.def')
        sleep(1)

        driver.find_element_by_xpath('//*[@id="L"]/option[24]').click()  # Seleciona conteúdo em linha
        sleep(1)

        driver.find_element_by_xpath('//*[@id="C"]/option[7]').click()  # Seleciona distritos em coluna
        sleep(1)

        driver.find_element_by_xpath('//*[@id="I"]/option[1]').click()  # Seleciona partos em conteúdo
        sleep(1)
        driver.find_element_by_xpath('//*[@id="I"]/option[2]').click()
        sleep(1)

        driver.find_element_by_xpath('//*[@id="A"]/option[1]').click()  # Seleciona o ano em períodos disponíveis
        sleep(1)
        driver.find_element_by_xpath('//*[@id="A"]/option[1]').click()
        sleep(1)

        driver.find_element_by_xpath('//*[@id="fig2"]').click()  # Seleciona o mês
        sleep(1)
        driver.find_element_by_xpath('//*[@id="S2"]/option[6]').click()
        sleep(1)

        driver.find_element_by_xpath('/html/body/center/div/form/div[4]/div[2]/div[2]/input[1]').click()  # Clica em mostrar
        sleep(1)

        try:
            element = driver.find_element_by_xpath('/html/body/table[2]/tbody')
            return element.get_attribute('outerHTML')
        except NoSuchElementException:
            print("Nenhum registro encontrado")
            return None

    def parse_data(html):
        """Faz o parsing do HTML e retorna os vetores de dados."""
        if not html:
            return []

        soup = BeautifulSoup(html, "html.parser")
        rows = soup.find_all("tr")
        all_vectors = []

        for row in rows:
            cells = row.find_all("td")
            data = [cell.get_text(strip=True).replace("-", "0") for cell in cells]
            all_vectors.append(data)

        return all_vectors

    def insert_data_to_mysql(vectors):
        """Insere os vetores de dados no banco de dados MySQL."""
        if not vectors:
            return

        connection = mysql.connector.connect(
            host="195.179.239.102",
            user="u165539734_sinascsp",
            password="Sinasc@sp24",
            database="u165539734_sinascsp"
        )

        cursor = connection.cursor()

        current_month = datetime.now().strftime("%Y-%m-%d")

        for vector in vectors:
            if vector:
                vector.append(current_month)
                values = ', '.join("'" + item + "'" for item in vector)
                sql = f"INSERT INTO tst_ods_dados_sexo VALUES ({values})"
                cursor.execute(sql)

        connection.commit()
        connection.close()
        return 'SUCESSO'
    
    def main():
        """Função principal."""
        driver = setup_driver()
        html = extract_data(driver)
        vectors = parse_data(html)
        insert_data_to_mysql(vectors)
        driver.quit()

    if __name__ == "__main__":
        main()

    pass


"""Verifica se tem dados no mês"""

def check_ods_result():
    # Obtém o resultado da tarefa 'ods'
    ods_result = extract_and_load_data()
    # Verifica se o resultado é diferente de "Nenhum registro encontrado"
    if ods_result == 'SUCESSO':
        return 'stg'  # Retorna o ID da tarefa 'stg'
    else:
        return 'dummy_task'  # Retorna o ID da tarefa dummy




dag = DAG(
    'sinasc_data_sexo',
    default_args=default_args,
    description='A DAG to extract and load data from website to MySQL',
    schedule_interval='@daily',
    start_date=datetime(2024, 4, 13),
    catchup=False,
    template_searchpath='/opt/airflow/sql'
)


#Tasks:


#Ods
ods = PythonOperator(
    task_id='ods',
    python_callable=extract_and_load_data,
    dag=dag,
)
#BIFURCA Sucess e insucess
branch_task = BranchPythonOperator(
    task_id='branch_task',
    python_callable=check_ods_result,
    provide_context=True,
    dag=dag,
)

#Encerra caso n tenha dados
dummy_task = DummyOperator(
    task_id='dummy_task',
    dag=dag,
)

#stage
stg = MySqlOperator(
    task_id='stg',
    mysql_conn_id='Mysql_Sinasc',  # Use o Conn Id configurado anteriormente
    sql='insert_st_dados_sexo_sinasc.sql',  # O arquivo SQL com o script de inserção
    dag=dag,
)


#Fluxo
ods >> branch_task
branch_task >> [stg, dummy_task]
