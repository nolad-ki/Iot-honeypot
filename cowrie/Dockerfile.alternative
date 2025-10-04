FROM python:3.11-slim

# Set environment variables  
ENV COWRIE_HOME=/cowrie
ENV PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev \
    openssh-client \
    telnet \
    && rm -rf /var/lib/apt/lists/*

WORKDIR $COWRIE_HOME

# Copy Cowrie files
COPY cowrie-git/ $COWRIE_HOME/

# Install dependencies directly without building the package
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Install Cowrie in development mode without version check
RUN pip install --no-cache-dir -e . --no-build-isolation

# Create directories
RUN mkdir -p /cowrie-data
RUN mkdir -p var/log/cowrie

# Create a simple startup script
RUN echo '#!/bin/bash\n\
cd /cowrie\n\
if [ ! -f "etc/cowrie.cfg" ]; then\n\
    cp etc/cowrie.cfg.dist etc/cowrie.cfg\n\
fi\n\
exec twistd --nodaemon --pidfile= cowrie' > /start-cowrie.sh && \
    chmod +x /start-cowrie.sh

EXPOSE 2222 2223

CMD ["/start-cowrie.sh"]
