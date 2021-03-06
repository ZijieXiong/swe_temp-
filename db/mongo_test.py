"""
Get used to pymongo!
"""
import db_connect as dbc

COLLECT_NAME = 'email'


client = dbc.get_client()
print(f"{client=}")

this_collect = client[dbc.db_nm][COLLECT_NAME]

insert_ret = this_collect.insert_many([{'filter_nm': 'bar1'},
                                      {'filter_nm': 'bar2'},
                                      {'filter_nm': 'bar3'},
                                      {'filter_nm': 'bar4'},
                                      {'filter_nm': 'bar5'}])
insert_ret = this_collect.insert_one({'trees': 'yellow leaves'})
print(f"{insert_ret=}")

docs = client[dbc.db_nm][COLLECT_NAME].find()
print(f"{docs=}")
for doc in docs:
    print(f"{doc=}")

docs = dbc.fetch_all_id(COLLECT_NAME)

doc = client[dbc.db_nm][COLLECT_NAME].find_one({'trees': 'yellow leaves'})
print(f"find one = {doc=}")

doc = client[dbc.db_nm][COLLECT_NAME].delete_many({'foo': 'bar'})
print(f"find one = {doc=}")

docs = client[dbc.db_nm][COLLECT_NAME].find()
for doc in docs:
    print(f"{doc=}")
