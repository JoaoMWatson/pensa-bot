import os
# import bot.database as database

from datetime import datetime
from dotenv import load_dotenv
from discord.utils import find
from discord.ext import commands
from bot.cogs.quotes import Quote
from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument

load_dotenv()

TIME_NOW = datetime.now()
TOKEN = os.getenv('DISCORD_TOKEN')


class PensaBot(commands.Bot):

    def __init__(self, command_prefix, self_bot):
        commands.Bot.__init__(
            self, command_prefix=command_prefix, self_bot=self_bot)
        self.add_event()
        self.add_commands()

    async def error_handler(self, command, error, ctx):
        with open('err.log', 'a') as f:
            f.write(
                f"Erro no comando '{command}' - Erro: {error} - timestamp: {TIME_NOW}\n")

        message = self.controller.error_embed(
            error="Cometemos um erro :/ - Contate algum ADM")

        await self.send_messages(message, ctx)

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
        self.add_cog(Quote(self))


def main():
    bot = PensaBot(command_prefix='?', self_bot=False)
    bot.run(TOKEN)
