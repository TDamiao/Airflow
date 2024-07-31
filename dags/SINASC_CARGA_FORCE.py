from airflow import DAG
from airflow.operators.mysql_operator import MySqlOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'SINASC_CARGA_FORCE',
    default_args=default_args,
    description='A simple DAG to test MySQL connection',
    schedule_interval='@once',
    start_date=days_ago(1),
    catchup=False,
    template_searchpath = '/opt/airflow/sql',
    
)


stg = MySqlOperator(
    task_id='stg',
    mysql_conn_id='Mysql_Sinasc',
    sql='insert_st_dados_sexo_sinasc.sql',
    dag=dag,
)

dw = MySqlOperator(
    task_id='dw',
    mysql_conn_id='Mysql_Sinasc',
    sql='insert_dw_dados_sexo_sinasc.sql', 
    dag=dag,
)

stg >> dw
