/*Iniciar servidor*/
python manage.py runserver

/*Iniciar redis*/
#No diretorio do arquivo
.\redis-server.exe
redis-cli.exe -h 127.0.0.1 -p 6379 ping

/*Dependencias a instalar*/
#instalar o python
get-pip.py
py -m pip install Django==5.2.5
pip install redis
#Instar o memurai






