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

    def pensamento(self):
        quotes = list(self.db.get_all_quotes())

        response = random.choice(quotes)

        embed = discord.Embed(title='Pensamento',
                              description=response['quote'], color=random.choice(self._COLOR_SET))

        embed.set_author(name=response['author'], url='')

        return embed

    def autor(self, ctx, autor):
        try:
            quotes = self.db.get_author_info(autor)

            embed = discord.Embed(title="Frases de " + autor,
                                  color=random.choice(self._COLOR_SET))
            embed.set_author(name=f'@{ctx.author}')

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
