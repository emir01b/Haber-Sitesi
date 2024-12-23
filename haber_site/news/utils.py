from pymongo import MongoClient
from decouple import config
import certifi

def get_db_handle():
    try:
        # SSL sertifikası ile bağlantı
        client = MongoClient(config('MONGODB_URI'), tlsCAFile=certifi.where())
        db = client['haber_db']
        # Test connection
        client.server_info()
        print("MongoDB bağlantısı başarılı!")
        return db, client
    except Exception as e:
        print(f"MongoDB bağlantı hatası: {e}")
        return None, None

def get_collection_handle(collection_name):
    db, client = get_db_handle()
    if db is None:
        return None, None
    return db[collection_name], client
