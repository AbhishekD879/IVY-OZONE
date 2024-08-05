import pymongo


def mongo_db_client_init(context):
    mongo_url = context.config.userdata.get('mongo_url', 'mongodb://localhost:27017/')
    mongo_username = context.config.userdata.get('mongo_username', '')
    mongo_password = context.config.userdata.get('mongo_password', '')
    mongo_db_client = pymongo.MongoClient(mongo_url,
                                          username=mongo_username,
                                          password=mongo_password)
    return mongo_db_client
