FROM python:3.9

RUN apt-get install wget
RUN pip install pandas SQLAlchemy psycopg2

WORKDIR /app
COPY ingest.py pipeline.py

ENTRYPOINT [ "python", "pipeline.py" ]
