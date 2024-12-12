import discord
from discord import app_commands
import json

def parseToken():
    with open("configure.json") as read_file:
        file_data = json.load(read_file)
        print(type(file_data))
        return file_data["token"]

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print(f"I have enabled myself to live! My name is {client.user.name}.")
    await tree.sync()

@tree.command(name="hi", description="This is really just a test")
async def command_hi(interaction):
    await interaction.response.send_message("DannyHPb")
    
token = parseToken()
client.run(token)