import os
from pymongo import MongoClient, DESCENDING, ASCENDING
from dotenv import load_dotenv

load_dotenv()
PASSWORD = os.getenv('MONGO_PASSWORD')


class DataAccess:
    client = MongoClient("mongodb+srv://discordbot:"+PASSWORD +
                         "@pensa-bot.dcwas.mongodb.net/pensamentos?retryWrites=true&w=majority")
    db = client.pensamentos

    def __init__(self):
        pass

    def get_all_quotes(self):
        return list(self.db.pensamentos.find())

    def get_author_info(self, author):
        return list(self.db.pensamentos.find({'author': str(author)}))

    def _get_last_id(self):
        last = list(self.db.pensamentos.find().sort('public_id', DESCENDING).limit(1))[0]['public_id']
        return last
    
    def insert_new_quote(self, autor, frase):
        public_id = self._get_last_id() + 1
        formated_autor = str(autor).strip().upper()
        formated_quote = str(frase).strip()
        row = {'public_id': public_id,
               'author': formated_autor,
               'quote': formated_quote}

        insertion = self.db.pensamentos.insert_one(row)
        
        return public_id
