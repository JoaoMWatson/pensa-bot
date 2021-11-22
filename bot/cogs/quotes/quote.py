
import bot.cogs.quotes.model as database

from discord.ext import commands
from bot.cogs.quotes.controller import Controller 

class Quote(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.controller = self.controller_injection('890974556515360779')
    
    async def error_handler(self, command, error, ctx):
        with open('../../err.log', 'a') as f:
            f.write(
                f"Erro no comando '{command}' - Erro: {error}\n")

        message = self.controller.error_embed(
            error="Cometemos um erro :/ - Contate algum ADM")

        await self.send_messages(message, ctx)
    
    async def send_messages(self, message, ctx):
        await ctx.channel.send(f"<@{ctx.author.id}>")
        await ctx.send(embed=message)

    def controller_injection(self, guild_id: str):
        controller_functions = Controller(
            dataAccess=database.DataAccess(guild_id))
        return controller_functions
    
    @commands.command(name='id', help='Comando de configuração para melhor uso do bot')
    async def getguild(self, ctx):
        guild_id = ctx.message.guild.id
        self.controller = self.controller_injection(guild_id)

        await ctx.channel.send(f"<@{ctx.author.id}>")
        await ctx.channel.send("Agora o bot funcionara normalmente. Aproveite!!")

    @commands.command(name='pensa', help='Frase aleatoria. Parametro<opt>: Frase respectiva ao id :D')
    async def pensa(self, ctx, pensamento_id=None):
        try:
            if pensamento_id is None:
                message = self.controller.pensa()
            elif pensamento_id is not None:
                message = self.controller.pensa(pensamento_id)

            await self.send_messages(message, ctx)

        except Exception as e:
            raise(await self.error_handler('pensa', e, ctx))

    @commands.command(name='pensador', help='Listagem de frases desse autor. Parametro: nome do autor. ;)')
    async def pensador(self, ctx, autor=None):
        try:
            message = self.controller.pensador(autor=autor)
            await self.send_messages(message, ctx)

        except Exception as e:
            raise(await self.error_handler('pensador', e, ctx))

    @commands.command(name='pensaram', help='Registra novo pensamento. Parametro: "frase" "autor"')
    async def pensaram(self, ctx, frase, autor):
        try:
            message = self.controller.pensaram(autor, frase)
            await self.send_messages(message, ctx)

        except Exception as e:
            raise(await self.error_handler('pensaram', e, ctx))

    @commands.command(name='sophia', help='Dona de todo universo')
    async def sophia(self, ctx):
        try:
            await ctx.channel.send("Dona de tudo rainha da sabedoria e conhecimendo do universo, ser todo poderoso e divino", ctx)

        except Exception as e:
            raise(await self.error_handler('sophia', e, ctx))