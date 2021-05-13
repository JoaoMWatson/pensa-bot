import os
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = commands.Bot(command_prefix='?')


@client.event
async def on_ready():
    print('Ready :D')


@client.command()
async def embed(ctx):
    embed = discord.Embed(title='xaxael gostoso', url="",
                          description='34cm de pau', color=discord.Color.blue())
    await ctx.send(embed=embed)


@client.command()
async def pensa(ctx):
    if ctx.author == client.user:
        return

    quotes = [
        'odeio pobres :gamer:(eu sei que n existe aqui :D é só um teste n ta pronto ainda)',
        'Não tem problema você ser sulista, tipo, até tem, mas você precisar falar bah?'
    ]

    response = random.choice(quotes)

    embed = discord.Embed(title='Pensamento', url='',
                          description=f'{response}', color=discord.Color.blue())

    await ctx.send(embed=embed)


# @client.command()
# async def help(ctx):
#     response = """
#     - ?pensa "{frase}" -{autor} → Salvar frase
#         Retorna → "Grande pensamento salvo! id={id}"
#     - ?pensa {opt: autor} {opt: id} → Exibe quote
#         Retorna → {frase}
#     """
#     await ctx.send(response)


@client.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')


client.run(TOKEN)
