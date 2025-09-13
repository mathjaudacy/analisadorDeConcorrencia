/*Iniciar servidor*/
python manage.py runserver

/*Iniciar redis*/
#No diretorio do arquivo
.\redis-server.exe
redis-cli.exe -h 127.0.0.1 -p 6379 ping

/*Inicia o ollama, model: gemma:2b*/
ollama run gemma:2b


/*Dependencias a instalar*/
#instalar o python
pip install playwright
playwright install
get-pip.py
py -m pip install Django==5.2.5
pip install redis
pip install pandas 
pip install pyarrow
pip install mysqlclient
pip install psycopg2-binary


/*Banco de dados*/
python manage.py makemigrations 
python manage.py makemigrations siteweb

python manage.py migrate



O banco de dados utilizado foi o postgree





