# Time-based-SQL-Injeciton-Script

This is my first Python attack script, so it still requires parameterization. 
You need to actively modify the function used in the main part of the code and pass the parameters.


# Time
```bash
abc' or sleep(3) and 'a'='a
```

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

