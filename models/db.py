import pymongo
import os

def get_db():
    client = pymongo.MongoClient(os.getenv("MONGODB_URL"), tlsAllowInvalidCertificates=True)
    db = client["BlogSystem"]
    return db
