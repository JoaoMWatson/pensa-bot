import os
import random
import discord
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


@bot.command(name='pensamento', help='Frase iconica aleatoria')
async def pensamento(ctx):
    try:
        if ctx.author == bot.user:
            return

        message = command_funcs.pensamento()
        
        await ctx.channel.send(f"<@{ctx.author.id}>")
        await ctx.send(embed=message)

    except Exception as e:
        print(e)


@bot.command(name='autor', help='Paramentro: nome do autor. Listagem de frases desse autor')
async def autor(ctx, autor: str = ""):
    try:
        if ctx.author == bot.user:
            return

        message = command_funcs.autor(ctx, autor=autor)

        await ctx.channel.send(f"<@{ctx.author.id}>")
        await ctx.send(embed=message)

    except Exception as e:
        print(e)


@bot.command(name='registrar', help='Registra novo pensamento :D')
async def registrar(ctx, frase, autor):
    try:
        if ctx.author == bot.user:
            return

        message = command_funcs.registrar(ctx, autor, frase)

        await ctx.channel.send(f"<@{ctx.author.id}>")
        await ctx.send(embed=message)
    except Exception as e:
        print(e)


@bot.command(name='test')
async def test(ctx, arg):
    await ctx.send(f'{arg=}')


@bot.event
async def on_command_error(event, *args, **kwargs):
    with open('err.txt', 'a') as f:
        f.write(f'\nUnhandled message: {args[0]} - timestamp: {TIME_NOW}')
    print(args)


def main():
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
