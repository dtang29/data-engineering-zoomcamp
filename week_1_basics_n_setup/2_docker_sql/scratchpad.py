
services:
  postgres:
    image: postgres:13
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
      POSTGRES_DB: airflow
    volumes:
      - postgres-db-volume:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "airflow"]
      interval: 5s
      retries: 5
    restart: always

#create docker with postgres manually
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v "/c:/Desktop/Projects/data-engineering-zoomcamp/2_docker_sql/ny_taxi_postgres_data:/var/lib/postgresql/data" \
  -p 5432:5432 \
  --network=pg-network \
  --name pg-database \
  postgres:13

#create docker with pgadmin
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pgadmin2 \
  dpage/pgadmin4

#After creating 2 docker images, we needed to go to jupyter notebook to read in the csv, iterate through it in chunks and upload to database
##Issues: Was having trouble getting wget on windows. Needed to download the binaries and dependencies and manually replace it in Git Bash's directory. 

#Network. This network thing is only used for local testing. In real world, you would connect to a real database that is on a cloud, not pg-database
docker network create pg-network

#Create a docker with postgres using python file. Refer to ingest.py. 
# URL="https://s3.amazonaws.com/nyc-tlc/trip+data/yellow_tripdata_2021-01.csv"

URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

python ingest.py \
    --user=root \
    --password=root \
    --host=localhost \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=${URL}

#Dockerizing the ingestion script. Now we build an image for the ingestion script.

docker build -t taxi_ingest:v001 .

URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

docker run --network=pg-network \
  taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --table_name=yellow_taxi_trips \
    --url=${URL}

#In python there is a simple http server code. You can set up a server that contains a directory to your desktop files and reference that URL to wget. 
#If you go to localhost:8000, you can have access to the directory

python -m http.server
