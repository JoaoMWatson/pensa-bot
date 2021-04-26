import os 
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
client = discord.Client()

@client.event
async def on_ready():    
    print(f'{client.user.name} has connected to discordo top')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(f'Salve {member.name} bem vindo cachorro muito ICE')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to my Discord server!'
    )

client.run(TOKEN)