from datetime import datetime

from discord.ext import commands

import bot.cogs.quotes.model as database
from bot.cogs.quotes.controller import Controller

TIME_NOW = datetime.now()

# TASK - Melhorar mensagens de erro e respostas a comandos
class Quote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.controller = self.controller_injection('308728057164857354')

    async def error_handler(self, ctx):
        message = self.controller.error_embed(
            error='Verifique novamente o uso do comando. ?help <comando> para saber mais'
        )

        await self.send_messages(message, ctx)

    async def send_messages(self, message, ctx):
        await ctx.channel.send(f'<@{ctx.author.id}>')
        await ctx.send(embed=message)

    def controller_injection(self, guild_id: str):
        controller_functions = Controller(
            dataAccess=database.DataAccess(guild_id)
        )
        print(f'Controller injected for guild {guild_id}')
        return controller_functions

    @commands.command(
        name='configura', help='Comando de configuração para melhor uso do bot'
    )
    async def get_guild(self, ctx):
        guild_id = ctx.message.guild.id
        self.controller = self.controller_injection(guild_id)

        print(f'getGuild for guild {guild_id}')


        await ctx.channel.send(f'<@{ctx.author.id}>')
        await ctx.channel.send(
            'Agora o bot funcionara normalmente. Aproveite!!'
        )

    @commands.command(
        name='pensa',
        help='Trás uma frase aleatória caso não informe o id. Parâmetro<opcional>: Frase respectiva ao id',
    )
    async def pensa(self, ctx, pensamento_id=None):
        try:
            if pensamento_id is None:
                message = self.controller.pensa()
            elif pensamento_id is not None:
                message = self.controller.pensa(pensamento_id)

            await self.send_messages(message, ctx)

        except Exception as e:
            raise (await self.error_handler('pensa', e, ctx))

    @commands.command(
        name='pensador',
        help='Listagem de frases desse autor. Parâmetro: nome do autor. ;)',
    )
    async def pensador(self, ctx, autor=None):
        try:
            message = self.controller.pensador(autor=autor)
            await self.send_messages(message, ctx)

        except Exception as e:
            raise (await self.error_handler('pensador', e, ctx))

    @commands.command(
        name='pensaram',
        help='Registra novo pensamento, necessário uso de aspas. Parâmetro: <"frase"> <"autor">',
    )
    async def pensaram(self, ctx, frase, autor):
        try:
            message = self.controller.pensaram(autor, frase)
            await self.send_messages(message, ctx)

        except Exception as e:
            raise (await self.error_handler('pensaram', e, ctx))

    async def setup(client):
        print('Creating Cog "Quote"')
        await client.add_cog(Quote(client))
