import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
PASSWORD = os.getenv('MONGO_PASSWORD')


class DataAccess:
    client = MongoClient("mongodb+srv://discordbot:"+PASSWORD +
                         "@pensa-bot.dcwas.mongodb.net/pensamentos?retryWrites=true&w=majority")
    db = client.pensamentos


    def get_all_quotes(self):
        return list(self.db.pensamentos.find())


    def get_author_info(self, author):
        return list(self.db.pensamentos.find({'author':str(author)}))
