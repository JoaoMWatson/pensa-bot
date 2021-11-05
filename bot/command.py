import os
from discord.ext import commands
from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument
from dotenv import load_dotenv
from bot.controller import Command
from bot.database import DataAccess
from datetime import datetime

load_dotenv()

TIME_NOW = datetime.now()
TOKEN = os.getenv('DISCORD_TOKEN')


class PensaBot(commands.Bot):
    def __init__(self, command_prefix, self_bot):
        commands.Bot.__init__(
            self, command_prefix=command_prefix, self_bot=self_bot)
        self.message1 = "[INFO]: Online FML"
        self.add_commands()

    async def on_ready(self):
        print(self.message1)

    async def send_messages(self, message, ctx):
        await ctx.channel.send(f"<@{ctx.author.id}>")
        await ctx.send(embed=message)

    def command_injection(self, guild):
        command_funcs = Command(dataAccess=DataAccess(guild=guild))
        return command_funcs

    def add_commands(self):
        try:
            @self.command(name='pensa', help='Frase aleatoria. Parametro<opt>: Frase respectiva ao id :D')
            async def pensa(ctx, pensamento_id=None):
                try:
                    commands = self.command_injection(guild=ctx.message.guild.id)

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
            async def pensador(ctx, autor: str = ""):
                try:
                    commands = self.command_injection(guild=ctx.message.guild.id)

                    message = commands.autor(ctx, autor=autor)

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

                commands = self.command_injection(guild=ctx.message.guild.id)
                message = commands.registrar(ctx, autor, frase)

                await self.send_messages(message, ctx)

            @self.event
            async def on_command_error(ctx, error):
                commands = self.command_injection(guild=ctx.message.guild.id)

                if error == CommandNotFound:
                    message = commands.error_embed(
                        error="Comando não encontrado :/")
                    await self.send_messages(message, ctx)

                if error == MissingRequiredArgument:
                    message = commands.error_embed(
                        error="Falta algum parametro :C")
                    await self.send_messages(message, ctx)
        except Exception as e:
            print(e)


def main():
    bot = PensaBot(command_prefix='?', self_bot=False)
    bot.run(TOKEN)
