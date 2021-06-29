import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
from database import DataAccess

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
COLOR_SET = (0xff5733, 0x64ff33, 0x33ffe9,
             0x2bb675, 0xe8159e, 0xf4b4de, 0x7346f8)


bot = commands.Bot(command_prefix='?')


@bot.event
async def on_ready():
    print('Ready :D')


@bot.command(name='quote')
async def pensamento(ctx):
    if ctx.author == bot.user:
        return

    db = DataAccess()

    quotes = list(db.get_all_quotes())

    response = random.choice(quotes)

    embed = discord.Embed(title='Pensamento',
                          description=response['quote'], color=random.choice(COLOR_SET))
    embed.set_author(name=response['author'], url='')

    await ctx.send(embed=embed)


@bot.command(name='register')
async def registrar(ctx, autor, frase):
    if ctx.author == bot.user:
        return



@bot.command(name='test')
async def test(ctx, arg):
    await ctx.send(f'{arg=}')


@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.txt', 'a') as f:
        f.write(f'\nUnhandled message: {args[0]}')


def main():
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
