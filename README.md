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





---- INstalar o gogole chrome 


1. Instalar o unzip
Você tentou descompactar o arquivo chromedriver_linux64.zip, mas o comando unzip não está instalado. Vamos instalar o unzip primeiro:

bash
Copiar código
apt-get install -y unzip
2. Descompactar o ChromeDriver
Agora que o unzip está instalado, descompacte o chromedriver_linux64.zip:

bash
Copiar código
unzip chromedriver_linux64.zip
Isso deve criar o arquivo chromedriver.

3. Mover o ChromeDriver
Depois de descompactar o arquivo, mova o chromedriver para o diretório correto:

bash
Copiar código
mv chromedriver /usr/local/bin/
4. Verificar o Google Chrome
Se o Google Chrome não está instalado no container, você precisará instalá-lo. Normalmente, você pode adicionar o repositório do Google e instalar o Chrome com os seguintes comandos:

bash
Copiar código
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome-stable_current_amd64.deb
apt-get install -f
5. Verificar a Instalação
Após essas etapas, verifique se o chromedriver e o google-chrome estão instalados corretamente:

bash
Copiar código
chromedriver --version
google-chrome --version
Se ambos estiverem instalados corretamente, você deve ver suas versões.



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
