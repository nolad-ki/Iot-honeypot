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
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR $COWRIE_HOME

# Copy Cowrie files
COPY cowrie-git/ $COWRIE_HOME/

# First upgrade pip
RUN pip install --no-cache-dir --upgrade pip

# Install requirements one by one to avoid dependency conflicts
RUN pip install --no-cache-dir twisted==22.10.0
RUN pip install --no-cache-dir cryptography==3.4.8
RUN pip install --no-cache-dir pyopenssl==22.1.0
RUN pip install --no-cache-dir attrs
RUN pip install --no-cache-dir service_identity
RUN pip install --no-cache-dir configparser
RUN pip install --no-cache-dir python-dateutil

# Try to install cowrie without the problematic dependency resolution
RUN cd $COWRIE_HOME && python setup.py install

# Create directories
RUN mkdir -p /cowrie-data
RUN mkdir -p var/log/cowrie

# Ensure the configuration file exists
RUN if [ ! -f "etc/cowrie.cfg" ]; then \
        cp etc/cowrie.cfg.dist etc/cowrie.cfg; \
    fi

# Use the direct Python approach
CMD ["python", "src/cowrie/scripts/cowrie.py", "start", "--nodaemon"]
