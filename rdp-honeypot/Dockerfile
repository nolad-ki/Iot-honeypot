FROM python:3.9-slim

WORKDIR /app

RUN pip install pyrdp

COPY rdp_honeypot.py .

EXPOSE 3389

CMD ["python", "rdp_honeypot.py"]
