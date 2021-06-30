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


@bot.command(name='pensamento', help='Frase iconica aleatoria')
async def pensamento(ctx):
    try:
        if ctx.author == bot.user:
            return

        db = DataAccess()

        quotes = list(db.get_all_quotes())

        response = random.choice(quotes)

        embed = discord.Embed(title='Pensamento',
                              description=response['quote'], color=random.choice(COLOR_SET))
        embed.set_author(name=response['author'], url='')

        await ctx.send(embed=embed)

    except Exception as e:
        on_error(e)


@bot.command(name='autor', help='Paramentro: nome do autor. Listagem de frases desse autor')
async def autor(ctx, autor: str):
    try:
        if ctx.author == bot.user:
            return

        db = DataAccess()
        quotes = db.get_author_info(autor)

        embed = discord.Embed(title="Frases de " + autor,
                              color=random.choice(COLOR_SET))
        embed.set_author(name=f'@{ctx.author}')

        if quotes:
            for quote in quotes:
                embed.add_field(
                    name=f"Id: {quote['public_id']}", value=quote['quote'], inline=False)

        else:
            embed.add_field(
                name=f"Autor não possui nenhuma frase :/", 
                value="Aproveite para salvar um lindo pensamento", inline=False
            )

        embed.set_footer(text="enjoy!")

        await ctx.send(embed=embed)

    except Exception as e:
        embed = discord.Embed(title="Erro :C",
                              color=0x000000)
        print(e)
        await ctx.send(embed=embed)


@bot.command(name='registrar')
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
