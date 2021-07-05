import random
import discord
from discord.ext.commands.errors import MissingRequiredArgument
from database import DataAccess


class Command:
    db = DataAccess()
    _COLOR_SET = (0xff5733, 0x64ff33, 0x33ffe9,
                  0x2bb675, 0xe8159e, 0xf4b4de, 0x7346f8)
    

    def __init__(self):
        pass

    def pensa(self, id=None):
        if id == None:
            _last_id = self.db._get_last_id()
            id = random.randint(1, _last_id)
        
        response = self.db.get_by_id(int(id))[0]

        embed = discord.Embed(title=f'Autor: ' + response['author'].capitalize(),
                              description=f'"{response["quote"]}"', color=random.choice(self._COLOR_SET))

        embed.set_author(name="Pensamento", url='')

        return embed

    def autor(self, ctx, autor):
        try:
            quotes = self.db.get_author_info(str(autor).upper())

            embed = discord.Embed(title="Frases de " + autor,
                                  color=random.choice(self._COLOR_SET))

            if quotes:
                for quote in quotes:
                    embed.add_field(
                        name=f"Id: {quote['public_id']}", value=quote['quote'], inline=False)

            else:
                embed.add_field(
                    name=f"Autor não possui nenhuma frase :/",
                    value="Aproveite para salvar um lindo pensamento", inline=False
                )

            embed.set_footer(text="enjoy!")

            return embed
        except Exception as e:
            print(e)

    def registrar(self, ctx, autor, frase):
        confirm = self.db.insert_new_quote(autor, frase)
        if confirm:
            embed_success = discord.Embed(
                title=f'public_id: {confirm}', color=random.choice(self._COLOR_SET))
            embed_success.set_author(name="Frase inserida com sucesso")

            return embed_success

        else:
            embed_error = discord.Embed(title="Tente novamente",
                                        color=discord.Color.red)
            embed_error.set_author(name="Erro ao inserir frase :/")

            return embed_error
