import random

import discord


class Controller:
    _COLOR_SET = (0x64FF33, 0x33FFE9, 0x2BB675, 0xE8159E, 0xF4B4DE, 0x7346F8)

    def __init__(self, dataAccess):
        self.db = dataAccess

    def pensa(self, id=None):
        try:
            if id == None:
                id = self.db.get_random_guild_quote_id()
            
            response = self.db.get_by_id(int(id))[0]
            embed = discord.Embed(
                description=f'Autor: ' + response['author'].capitalize(),
                title=f'"{response["quote"]}"',
                color=random.choice(self._COLOR_SET),
            )
            embed.set_author(name='Pensamento', url='')

            return embed
        except Exception as e:
            return self.error_embed(error='Não foi possível retornar frase desejada.')

    def pensador(self, autor):
        try:
            quotes = self.db.get_author_info(str(autor).upper())

            embed = discord.Embed(
                title='Frases de ' + autor,
                color=random.choice(self._COLOR_SET),
            )

            if quotes:
                for quote in quotes:
                    embed.add_field(
                        name=f"Id: {quote['public_id']}",
                        value=quote['quote'],
                        inline=False,
                    )
            else:
                embed.add_field(
                    name=f'Autor não possui nenhuma frase :/',
                    value='Aproveite para salvar um lindo pensamento',
                    inline=False,
                )

            return embed
        except Exception as e:
            return self.error_embed(error='Não foi possível retornar autor.')


    def pensaram(self, autor, frase):
        confirm = self.db.insert_new_quote(autor, frase)
        if confirm:
            embed_success = discord.Embed(
                title='Frase inserida com sucesso',
                color=random.choice(self._COLOR_SET),
            )
            embed_success.set_author(name=f'ID: {confirm}')

            return embed_success

        else:
            self.error_embed(error='Não foi possível inserir a frase.')

    def error_embed(self, error):
        embed = discord.Embed(title=error, color=0xFF000)
        embed.set_author(name='Aconteceu um erro :/')

        return embed
