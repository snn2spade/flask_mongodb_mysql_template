# GETTING STATED
## Run as Local
### Prerequisite
```
python >= 3.7
mongodb >= 4.2
```
### setup python virtual env
```
pip install virtualenv
virtualenv venv
source venv/bin/activate
pip install -r requirements.txt
```
### run test
```
pytest
```
### generate test coverage report
```
coverage run --source=app -m pytest
coverage report
```
then you can open report on `htmlcov/index.html`
### create new configuration file
```
cp app_config.example.json app_config.json
nano app_config.json
```
### edit the MongoDB connection
```
"MONGO": {
  "HOST": "[MONGO_HOST]",
  "USERNAME": "[MONGO_USERNAME]",
  "PASSWORD": "[MONGO_PASSWORD]",
  "DB_NAME": "[MONGO_DB_NAME]",
  "AUTH_DB_NAME": "[MONGO_AUTH_DB_NAME]"
}
```
### run migration script
```
python migrate.py
```
### run Flask server
```
python -m app.app
```
then open browser and go to http://localhost:5000/info 
## Run with Docker-compose
### Prerequisite
```
docker >= 19.03
```
### Start docker
```
docker-compose up -d --build
```
then open browser and go to http://localhost:5000/info 