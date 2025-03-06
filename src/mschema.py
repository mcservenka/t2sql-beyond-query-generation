import os
import json
from sqlalchemy import create_engine

from external.mschema.schema_engine import SchemaEngine
from external.mschema.m_schema import MSchema

from src.utils import get_dev_dbs
from configs.paths import MSCHEMAS_PATH, SPIDER_DATABASE_PATH, BIRD_DATABASE_PATH


# Reference: https://github.com/XGenerationLab/M-Schema



class MschemaCreator:

    # inits mschema object for dataset and calls create_mschema_json
    def __init__(self, dataset:str = "spider"):

        self.dataset = dataset
        if dataset == "spider":
            self.db_path = SPIDER_DATABASE_PATH
        elif dataset == "bird":
            self.db_path = BIRD_DATABASE_PATH
         
        
        os.makedirs(MSCHEMAS_PATH, exist_ok=True)
        os.makedirs(f"{MSCHEMAS_PATH}{dataset}", exist_ok=True)
        self.dbs = get_dev_dbs(dataset=dataset)

        for db in self.dbs:
            output_path = f"{MSCHEMAS_PATH}{dataset}/{db}/"
            os.makedirs(output_path, exist_ok=True)
            self.create_mschema(db_id=db, path=output_path)
        
        print(f"MSchemas of {self.dataset} ready.")


    # create mschema json and txt
    def create_mschema(self, db_id:str = None, path: str = None):
        
        # database connection
        db_path = f"{self.db_path}{db_id}/{db_id}.sqlite"
        abs_path = os.path.abspath(db_path)
        db_engine = create_engine(f"sqlite:///{abs_path}")
        
        # create mschema
        schema_engine = SchemaEngine(engine=db_engine, db_name=db_id)
        mschema = schema_engine.mschema
        mschema_str = mschema.to_mschema()

        # save output
        mschema.save(f"{path}{db_id}.json")
        with open(f"{path}{db_id}.txt", "w", encoding="utf-8") as f: f.write(mschema_str)
        

    # load mschema string from json
    def read_mschema_json(self, db_id: str = None):

        ms_path = f"{MSCHEMAS_PATH}{self.dataset}/{db_id}.json"

        ms = MSchema(db_id=db_id)
        ms.load(ms_path) # loads all parameters into mschema object

        return ms.to_mschema()


