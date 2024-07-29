# airflow_v2

Site da documentação: 
https://airflow.apache.org/docs/apache-airflow/2.0.2/start/docker.html

*Não tem a pasta Sql na doc oficial eu mapeio para separar e organizar as inteligencias. 

Processo: 

1° Clone 
2° Criar Diretórios 
mkdir ./dags ./logs ./plugins ./sql
3° Libera Acesso
echo -e "AIRFLOW_UID=$(id -u)\nAIRFLOW_GID=0" > .env


--- BKP 



sudo pip install docker-compose docker-compose --version >2.2 pip show docker-compose | grep "Location:" export PATH="$PATH:/home/user/.local/bin" source ~/.bashrc

git clone git@github.com:Foradocubo/airflow.git mkdir -p ./logs ./plugins ./config echo -e "AIRFLOW_UID=$(id -u)" > .env

docker-compose build --no-cache #Executar: docker-compose up airflow-init

#Executar: docker-compose up -d

#Executar: docker exec -it airflow-airflow-worker-1 /bin/bash

su - airflow

#Executar: pip install selenium

#Executar: pip install webdriver_manager

#Verifucar: docker ps
