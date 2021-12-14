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
cloud_db = "swe.njqsr.mongodb.net"
passwd = "Waffles"
# os.environ.get("MONGO_PASSWD", '')
cloud_mdb = "mongodb+srv"
db_params = "retryWrites=true&w=majority"
db_nm = "sweDB"

REMOTE = "0"
LOCAL = "1"

client = None


def get_client():
    """
    This provides a uniform way to get the client across all uses.
    Returns a mongo client object... maybe we shouldn't?
    Also set global client variable.
    """
    global client
    if os.environ.get("LOCAL_MONGO", REMOTE) == LOCAL:
        print("Connecting to Mongo locally")
        client = pm.MongoClient()
    else:
        print("Connecting to Mongo remotely")
        client = pm.MongoClient(f"{cloud_mdb}://{user_nm}:{passwd}.@{cloud_db}"
                                + f"/{db_nm}?{db_params}",
                                server_api=ServerApi('1'))
    return client


def fetch_one(collect_nm, filters={}):
    """
    Fetch one record that meets filters.
    """
    return client[db_nm][collect_nm].find_one(filters)


def del_one(collect_nm, filters={}):
    """
    Delete one record that meets filters.
    """
    return client[db_nm][collect_nm].delete_one(filters)


def fetch_all(collect_nm, key_nm):
    "Fetch all record in one sheet"
    all_docs = {}
    for doc in client[db_nm][collect_nm].find():
        print(doc)
        all_docs[doc[key_nm]] = json.loads(bsutil.dumps(doc))
    return all_docs


def insert_doc(collect_nm, doc):
    "Insert one record to a sheet"
    client[db_nm][collect_nm].insert_one(doc)
