FROM python:3.9-slim

WORKDIR /app

RUN pip install paramiko

COPY ssh_honeypot.py .

EXPOSE 2222

CMD ["python", "ssh_honeypot.py"]
