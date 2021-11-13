import os
from pymongo import MongoClient, DESCENDING
from dotenv import load_dotenv

load_dotenv()
PASSWORD = os.getenv('MONGO_PASSWORD')


class DataAccess:
    client = MongoClient(
        "mongodb+srv://discordbot:{}@pensa-bot.dcwas.mongodb.net/myFirstDatabase?retryWrites=true&w=majority".format(PASSWORD)).pensamentos

    def __init__(self, guild_id: str):
        self.db = self.client['quotes']
        self.guild_id = guild_id

    def get_all_quotes(self):
        return list(self.db.find({'guild': str(self.guild_id)}))

    def get_by_id(self, id):
        return list(self.db.find({'public_id': id,
                                  'guild': str(self.guild_id)}))

    def get_author_info(self, author):
        return list(self.db.find({'author': str(author),
                                  'guild': str(self.guild_id)}))

    def get_last_id(self):
        last = list(self.db.find().sort(
            'public_id', DESCENDING).limit(1))[0]['public_id']
        return int(last)

    def insert_new_quote(self, autor, frase):
        public_id = self.get_last_id() + 1
        formated_autor = str(autor).strip().upper()
        formated_quote = str(frase).strip()

        row = {'public_id': public_id,
               'author': formated_autor,
               'quote': formated_quote,
               'guild': str(self.guild_id)}

        self.db.insert_one(row)

        return public_id
