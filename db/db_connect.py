"""
This file contains some common MongoDB code.
"""
import os
import json
import pymongo as pm
import bson.json_util as bsutil
from pymongo.server_api import ServerApi

# all of these will eventually be put in the env:
user_nm = "Pancake"
cloud_db = "pancakeflippers.7bgdg.mongodb.net"
passwd = "Waffles"
# os.environ.get("MONGO_PASSWD", '')
cloud_mdb = "mongodb+srv"
db_params = "retryWrites=true&w=majority"
db_nm = "sweDB"

client = None


def get_client():
    """
    This provides a uniform way to get the client across all uses.
    Returns a mongo client object... maybe we shouldn't?
    Also set global client variable.
    """
    global client
    if os.environ.get("LOCAL_MONGO", False):
        client = pm.MongoClient()
    else:
        client = pm.MongoClient(f"mongodb+srv://{user_nm}:{passwd}.@{cloud_db}"
                                + f"/{db_nm}?{db_params}",
                                server_api=ServerApi('1'))
    return client


def fetch_all(collect_nm, key_nm):
    all_docs = {}
    for doc in client[db_nm][collect_nm].find():
        print(doc)
        all_docs[doc[key_nm]] = json.loads(bsutil.dumps(doc))
    return all_docs


def insert_doc(collect_nm, doc):
    client[db_nm][collect_nm].insert_one(doc)
