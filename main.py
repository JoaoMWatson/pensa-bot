import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

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

    quotes = {
        'odeio pobres :gamer:(eu sei que n existe aqui :D é só um teste n ta pronto ainda)',
        'Não tem problema você ser sulista, tipo, até tem, mas você precisar falar bah?',
    }

    response = random.choice(quotes)

    embed = discord.Embed(title='Pensamento',
                          description=f'{response}', color=discord.Color.blue())

    await ctx.send(embed=embed)

@bot.command(name='register')
async def registrar(ctx, autor, frase):
    if ctx.author == bot.user:
        return


bot.run(TOKEN)
