import pymongo
import os
from dotenv import load_dotenv
load_dotenv()

def get_db():
    client = pymongo.MongoClient(os.getenv("MONGODB_URL"), tlsAllowInvalidCertificates=True)
    db = client["BlogSystem"]
    return db
