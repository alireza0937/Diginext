FROM python:3.9-alpine
WORKDIR /app
COPY requirements.txt .
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
RUN apk add mariadb-connector-c-dev
RUN apk add \
    build-base \
    python3-dev \
    geos \
    geos-dev
RUN pip install -r requirements.txt
COPY . .
ENTRYPOINT ["/entrypoint.sh"]

