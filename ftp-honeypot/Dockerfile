FROM python:3.9-slim

WORKDIR /app

RUN pip install pyftpdlib

COPY ftp_honeypot_fixed.py .

EXPOSE 21

CMD ["python", "ftp_honeypot_fixed.py"]
