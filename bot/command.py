import os
import bot.database as database

from datetime import datetime
from dotenv import load_dotenv
from discord.ext import commands
from bot.controller import Command
from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument

load_dotenv()

TIME_NOW = datetime.now()
TOKEN = os.getenv('DISCORD_TOKEN')


class PensaBot(commands.Bot):
    guild_id = ""

    def __init__(self, command_prefix, self_bot):
        commands.Bot.__init__(
            self, command_prefix=command_prefix, self_bot=self_bot)
        self.add_event()
        self.add_commands()

    async def send_messages(self, message, ctx):
        await ctx.channel.send(f"<@{ctx.author.id}>")
        await ctx.send(embed=message)

    def command_injection(self):
        command_funcs = Command(
            dataAccess=database.DataAccess(guild='890974556515360779'))
        return command_funcs

    def add_event(self):
        @self.event
        async def on_ready():
            print("ON")

        @self.event
        async def on_error(event, *args, **kwargs):
            with open('err.log', 'a') as f:
                if event == 'on_message':
                    f.write(f'Unhandled message: {args[0]}\n')
                else:
                    raise

        @self.event
        async def on_command_error(ctx, error):
            print(error)
            if error == CommandNotFound:
                message = commands.error_embed(
                    error="Comando não encontrado :/")
                await self.send_messages(message, ctx)

            if error == MissingRequiredArgument:
                message = commands.error_embed(
                    error="Falta algum parametro :C")
                await self.send_messages(message, ctx)

    def add_commands(self):
        commands = self.command_injection()
        try:
            @self.command(name='pensa', help='Frase aleatoria. Parametro<opt>: Frase respectiva ao id :D')
            async def pensa(ctx, pensamento_id=None):
                try:
                    if pensamento_id is None:
                        message = commands.pensa()

                    elif pensamento_id is not None:
                        message = commands.pensa(pensamento_id)

                    await self.send_messages(message, ctx)

                except CommandNotFound:
                    message = commands.error_embed(
                        error="Comando não encontrado :/")
                    await self.send_messages(message, ctx)

                except MissingRequiredArgument:
                    message = commands.error_embed(
                        error="Falta algum parametro :C")
                    await self.send_messages(message, ctx)

            @self.command(name='pensador', help='Listagem de frases desse autor. Parametro: nome do autor. ;)')
            async def pensador(ctx, autor=None):
                try:
                    message = commands.autor(autor=autor)

                    await self.send_messages(message, ctx)

                except CommandNotFound:
                    message = commands.error_embed(
                        error="Comando não encontrado :/")
                    await self.send_messages(message, ctx)

                except MissingRequiredArgument:
                    message = commands.error_embed(
                        error="Falta algum parametro :C")
                    await self.send_messages(message, ctx)

            @self.command(name='pensaram', help='Registra novo pensamento. Parametro: "frase" "autor"')
            async def pensaram(ctx, frase, autor):
                message = commands.registrar(autor, frase)

                await self.send_messages(message, ctx)

        except Exception as e:
            print(e)

def main():
    bot = PensaBot(command_prefix='?', self_bot=False)
    bot.run(TOKEN)
