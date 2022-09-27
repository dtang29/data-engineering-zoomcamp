#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
from time import time
import argparse
import os
import gzip


def main(params):
    user = params.user 
    password = params.password 
    host = params.host
    port = params.port 
    db = params.db
    table_name = params.table_name
    url = params.url

    csv_name = 'output.csv.gz'

    os.system(f"wget {url} -O {csv_name} --no-check-certificate")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    # with gzip.open(csv_name, 'rb') as f: 
    #     df_iter = pd.read_csv(f, iterator=True, chunksize=100000)

    df_iter = pd.read_csv(csv_name, compression='gzip', header=0, sep=',', quotechar='"', iterator=True, chunksize=100000)
    # print(df.head())
    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)

    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')
    print('Appended headers')

    df.to_sql(name=table_name, con=engine, if_exists='append')
    print('Appended data!')

    while True: 
        t_start = time()
        print('Begin next append!')
        df = next(df_iter)
        
        df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
        df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
        
        df.to_sql(name=table_name, con=engine, if_exists='append')
        
        t_end = time()
        
        print('inserted another chunk..., took %.3f second' % (t_end - t_start))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--user', help='user name for pos') 
    parser.add_argument('--password', help='password for postgres')
    parser.add_argument('--host', help='host for postgres')
    parser.add_argument('--port', help='port for postgres')
    parser.add_argument('--db', help='database name for postgres')
    parser.add_argument('--table_name', help='name of the table where we will write the results to')
    parser.add_argument('--url', help='url of the csv file')

    args = parser.parse_args()

    main(args)




