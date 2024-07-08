# Time-based-SQL-Injeciton-Script

This is my first Python attack script, so it still requires parameterization. 
You need to actively modify the function used in the main part of the code and pass the parameters.


# Time-based-SQL-Injeciton
```
' or sleep(3)
abc' or sleep(3) and 'a'='a
```
It involves sending SQL queries to the database that force it to wait for a specified amount of time before responding. 
By measuring the server's response time, an attacker can infer whether certain conditions are true or false, thereby extracting information from the database without direct feedback.

# Docker
Build Enviroment on Ubuntu

And you will get a simple website that has a time-based SQL injection vulnerability.
```bash
chmod 744 *

docker-compose build

docker-compose up
```
Stop and Remove All Containers
```bash
docker stop $(docker ps -q)
docker rm $(docker ps -a -q)
```

