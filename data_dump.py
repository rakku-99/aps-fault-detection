import pymongo
import pandas as pd
import json
from sensor.config import mongo_client

# Provide the mongodb localhost url for ineuron to connect python to mongodb.
# client = pymongo.MongoClient("mongodb://localhost:27017/neurolabDB")

DATA_FILE_PATH= "/config/workspace/aps_failure_training_set1.csv"
DATABASE_NAME = 'aps'
COLLECTION_NAME ='sensor'

if __name__ == '__main__':
    df=pd.read_csv(DATA_FILE_PATH)
    #print(f"Rows and Columns:{df.shape}")
    print(f"Rows and Columns")

    # convert dataframe to json to dump records in mongo db
    df.reset_index(drop=True,inplace=True)
    
    json_record = list(json.loads(df.T.to_json()).values()) #convert str etc to json
    print(json_record[0])

    # insert converted record to mongoDB
    mongo_client[DATABASE_NAME][COLLECTION_NAME].insert_many(json_record)