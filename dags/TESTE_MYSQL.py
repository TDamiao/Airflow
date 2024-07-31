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
    'TESTE_MYSQL_SINASC',
    default_args=default_args,
    description='A simple DAG to test MySQL connection',
    schedule_interval='@once',
    start_date=days_ago(1),
    catchup=False,
    template_searchpath = '/opt/airflow/sql',
    
)


t1 = MySqlOperator(
    task_id='insert_stage',
    mysql_conn_id='Mysql_Sinasc',  # Use o Conn Id configurado anteriormente
    sql='Teste_Mysql.sql',
    dag=dag
)

t1
