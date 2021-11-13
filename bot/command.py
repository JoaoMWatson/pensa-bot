import os
import bot.database as database

from datetime import datetime
from dotenv import load_dotenv
from discord.utils import find
from discord.ext import commands
from bot.controller import Controller
from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument

load_dotenv()

TIME_NOW = datetime.now()
TOKEN = os.getenv('DISCORD_TOKEN')


class PensaBot(commands.Bot):
    guild_id = None

    def __init__(self, command_prefix, self_bot):
        commands.Bot.__init__(
            self, command_prefix=command_prefix, self_bot=self_bot)
        self.add_event()
        self.add_commands()
        self.controller = self.controller_injection('890974556515360779')

    async def send_messages(self, message, ctx):
        await ctx.channel.send(f"<@{ctx.author.id}>")
        await ctx.send(embed=message)

    def controller_injection(self, guild_id: str):
        controller_functions = Controller(
            dataAccess=database.DataAccess(guild_id))
        return controller_functions
    
    def error_handler(self, command, error):
        with open('err.log', 'a') as f:
            f.write(f"Erro no comando '{command}' - Erro: {error} - timestamp: {TIME_NOW}\n")

        message = self.controller.error_embed(
            error="Cometemos um erro :/ - Contate algum ADM")
        
        return message
        
    def add_event(self):
        @self.event
        async def on_ready():
            print("ON")

        @self.event
        async def on_guild_join(guild):
            general = find(lambda x: x.name ==
                           'geral' or 'general',  guild.text_channels)
            if general and general.permissions_for(guild.me).send_messages:
                await general.send('Olá {}! Por favor utilize o comando "?id" para configurar me configurar em seu servidor.'.format(guild.name))

        @self.event
        async def on_error(event, *args, **kwargs):
            with open('err.log', 'a') as f:
                f.write(f"Error: {args[0]} - timestamp: {TIME_NOW}\n")

        @self.event
        async def on_command_error(ctx, error):
            if error == CommandNotFound:
                message = commands.error_embed(
                    error="Comando não encontrado :/")
                await self.send_messages(message, ctx)

            if error == MissingRequiredArgument:
                message = commands.error_embed(
                    error="Falta algum parametro :C")
                await self.send_messages(message, ctx)

    def add_commands(self):
        try:
            @self.command(name='id', help='Comando de configuração para melhor uso do bot')
            async def getguild(ctx):
                guild_id = ctx.message.guild.id
                self.controller = self.controller_injection(guild_id)

                await ctx.channel.send(f"<@{ctx.author.id}>")
                await ctx.channel.send("Agora o bot funcionara normalmente. Aproveite!!")

            @self.command(name='pensa', help='Frase aleatoria. Parametro<opt>: Frase respectiva ao id :D')
            async def pensa(ctx, pensamento_id=None):
                try:
                    if pensamento_id is None:
                        message = self.controller.pensa()
                    elif pensamento_id is not None:
                        message = self.controller.pensa(pensamento_id)

                    await self.send_messages(message, ctx)

                except Exception as e:
                    self.error_handler('pensa', e)
                    await self.send_messages(message, ctx)


            @self.command(name='pensador', help='Listagem de frases desse autor. Parametro: nome do autor. ;)')
            async def pensador(ctx, autor=None):
                try:
                    message = self.controller.pensador(autor=autor)
                    await self.send_messages(message, ctx)

                except Exception as e:
                    self.error_handler('pensador', e)
                    await self.send_messages(message, ctx)

            @self.command(name='pensaram', help='Registra novo pensamento. Parametro: "frase" "autor"')
            async def pensaram(ctx, frase, autor):
                try:
                    message = self.controller.pensaram(autor, frase)
                    await self.send_messages(message, ctx)

                except Exception as e:
                    self.error_handler('pensaram', e)
                    await self.send_messages(message, ctx)

        except Exception as e:
            print(e)


def main():
    bot = PensaBot(command_prefix='?', self_bot=False)
    bot.run(TOKEN)
