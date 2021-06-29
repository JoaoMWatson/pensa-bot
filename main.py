import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
from database import DataAccess

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='?')


@bot.event
async def on_ready():
    print('Ready :D')


@bot.command(name='quote')
async def pensamento(ctx):
    if ctx.author == bot.user:
        return

    db = DataAccess()

    color_set = (0xff5733, 0x64ff33, 0x33ffe9,
                 0x2bb675, 0xe8159e, 0xf4b4de, 0x7346f8)

    quotes = db.get_all_quotes()

    response = quotes[random.randint(0, 1)]

    embed = discord.Embed(title='Pensamento',
                          description=response['quote'], color=random.choice(color_set))
    embed.set_author(name=response['author'], url='')

    await ctx.send(embed=embed)


@bot.command(name='register')
async def registrar(ctx, autor, frase):
    if ctx.author == bot.user:
        return


@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.txt', 'a') as f:
        f.write(f'\nUnhandled message: {args[0]}')


def main():
    bot.run(TOKEN)


if __name__ == '__main__':
    main()
