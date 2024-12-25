import discord
from discord import app_commands
import os
import json

def parseToken():
    with open("configure.json") as read_file:
        file_data = json.load(read_file)
        return file_data["token"]

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

@client.event
async def on_ready():
    print(f"Bot online as {client.user.name}.")
    await tree.sync()
    print("synced commands")

@tree.command(name="hi", description="This is really just a test")
async def command_hi(interaction):
    await interaction.response.send_message("DannyHPb")

@tree.command(name="info", description="About the bot")
async def command_info(interaction):
	await interaction.response.send_message("This bot was made to automate daily scrambles in the DannyHTv discord server. It was made and hosted by Digipr01. For any questions and suggestions, you can DM him.")

@tree.command(name="terminate", description="Shuts off the bot")
async def command_shutdown(interaction):
	await interaction.response.send_message("Shutting down DannyHTV bot")
	os._exit(os.EX_OK)
token = parseToken()
client.run(token)
