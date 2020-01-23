FROM snn2spade/python-with-git:3.6.8-slim

COPY app_config.json /code/
COPY logging_config.json /code/
COPY requirements.txt /code/
COPY /.git /code/.git/

WORKDIR /code
RUN pip install -r requirements.txt

COPY /app /code/app/
CMD ["python","-m", "app.app"]
