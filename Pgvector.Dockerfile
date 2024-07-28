# Use the official PostgreSQL 13 image as the base image
FROM postgres

# Install required packages
RUN apt-get update && apt-get install -y \
    build-essential \
    postgresql-server-dev-13 \
    git \
    && rm -rf /var/lib/apt/lists/*

# Clone the pgvector repository and install the extension
RUN git clone --branch v0.4.2 https://github.com/pgvector/pgvector.git \
    && cd pgvector \
    && make && make install \
    && cd .. && rm -rf pgvector
