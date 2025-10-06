FROM python:3.9-slim

WORKDIR /app

# Install dependencies
RUN pip install flask requests

# Copy the honeypot script
COPY http_honeypot.py .

# Expose HTTP port
EXPOSE 80

# Run the honeypot
CMD ["python", "http_honeypot.py"]
