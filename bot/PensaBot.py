from datetime import datetime

from discord import Intents
from discord.ext import commands
from discord.ext.commands.errors import (CommandNotFound,
                                         MissingRequiredArgument)
from discord.utils import find

from bot.cogs.quotes import Quote
from config import settings

import logging

TIME_NOW = datetime.now()
TOKEN = settings.DISCORD_TOKEN

# Melhorar help
class PensaBot(commands.Bot):
    def __init__(self, command_prefix, self_bot, intents):
        commands.Bot.__init__(
            self, command_prefix=command_prefix, self_bot=self_bot, intents=intents
        )
        self.add_event()
        self.add_commands()


    def add_event(self):
        @self.event
        async def on_ready():
            await self.add_cog(Quote(self))
            print(f'ON - timestamp: {TIME_NOW}')

        #TASK - não funciona Arrumar pfv
        @self.event
        async def on_guild_join(guild):
            print(f'Canais de texto - on guild join: {guild.text_channels}')
            general = guild.text_channels[0]
            if general and general.permissions_for(guild.me).send_messages:
                await general.send(
                    'Olá {}! Por favor utilize o comando "?configura" para configurar me configurar em seu servidor.'.format(
                        guild.name
                    )
                )

        @self.event
        async def on_command_error(ctx, error):
            if error == CommandNotFound:
                message = commands.error_embed(
                    error='Comando não encontrado :/'
                )
                await self.send_messages(message, ctx)

            if error == MissingRequiredArgument:
                message = commands.error_embed(
                    error='Falta algum parametro :C'
                )
                await self.send_messages(message, ctx)

    def add_commands(self):
        @self.command(name='status', help='Verifica o status do bot.')
        async def healthcheck(ctx):
            """Verifica o status do bot."""
            await ctx.send("Jovem livre e selvagem")


def main():
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    intents = Intents.default()
    intents.message_content = True
    intents.members = True

    bot = PensaBot(command_prefix='?', self_bot=False, intents=intents)
    bot.run(TOKEN, log_handler=handler)
