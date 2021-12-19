"""
This file contains some common MongoDB code.
"""
import os
import json
import pymongo as pm
import bson.json_util as bsutil
# from pymongo.server_api import ServerApi

# all of these will eventually be put in the env:
user_nm = "PANCAKE"
cloud_db = "swe.njqsr.mongodb.net"
passwd = "WAFFLE"
# os.environ.get("MONGO_PASSWD", '')
cloud_mdb = "mongodb+srv"
db_params = "retryWrites=true&w=majority"
db_nm = "sweDB"
if os.environ.get("TEST_MODE", ''):
    db_nm = "test_sweDB"

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
        client = pm.MongoClient(f"{cloud_mdb}://{user_nm}:{passwd}@{cloud_db}"
                                + f"/{db_nm}?{db_params}")
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
    all_docs = {}
    cursor = client[db_nm][collect_nm].find({})
    for doc in cursor:
        all_docs[doc[key_nm]] = json.loads(bsutil.dumps(doc))
    return all_docs


def fetch_all_id(collect_nm):
    """
    This method would return a dictionary use a completely new id as key
    """
    all_docs = {}
    cursor = client[db_nm][collect_nm].find({})
    i = 0
    for doc in cursor:
        all_docs[i] = json.loads(bsutil.dumps(doc))
        i = i + 1
    return all_docs


def insert_doc(collect_nm, doc):
    "Insert one record to a sheet"
    client[db_nm][collect_nm].insert_one(doc)
