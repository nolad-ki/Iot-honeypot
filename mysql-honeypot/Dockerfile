FROM python:3.9-slim

WORKDIR /app

RUN pip install mysql-connector-python

COPY mysql_honeypot.py .

EXPOSE 3306

CMD ["python", "mysql_honeypot.py"]
