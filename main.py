import os
from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument
from dotenv import load_dotenv
from commands import Command
from datetime import datetime

TIME_NOW = datetime.now()

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
command_funcs = Command()

bot = commands.Bot(command_prefix='?')


@bot.event
async def on_ready():
    print('Ready :D')


@bot.command(name='pensa', help='Frase iconica aleatoria')
async def pensa(ctx, id=None):
    if ctx.author == bot.user:
        return
    
    if id is None:
        message = command_funcs.pensa()
        
    elif id is not None:
        message = command_funcs.pensa(id)

    await ctx.channel.send(f"<@{ctx.author.id}>")
    await ctx.send(embed=message)


@bot.command(name='autor', help='Paramentro: nome do autor. Listagem de frases desse autor')
async def autor(ctx, autor: str = ""):

    if ctx.author == bot.user:
        return

    message = command_funcs.autor(ctx, autor=autor)

    await ctx.channel.send(f"<@{ctx.author.id}>")
    await ctx.send(embed=message)


@bot.command(name='registrar', help='Registra novo pensamento :D')
async def registrar(ctx, frase, autor):

    if ctx.author == bot.user:
        return

    message = command_funcs.registrar(ctx, autor, frase)

    await ctx.channel.send(f"<@{ctx.author.id}>")
    await ctx.send(embed=message)


@bot.command(name='test')
async def test(ctx, *args):
    await ctx.send(f'args {args[0]} ')


# @bot.event
# async def on_command_error(event, *args, **kwargs):
#     with open('err.txt', 'a') as f:
#         f.write(f'\nUnhandled message: {args[0]} - timestamp: {TIME_NOW}')
#     print(args)


def main():
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
