import discord
from discord import app_commands
import os
import json
import subprocess
from enum import Enum
import typing

def parseToken():
    with open("configure.json") as read_file:
        file_data = json.load(read_file)
        return file_data["token"]

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

AverageTypes = {
	"Single": 1,
	"Mo3": 3,
	"Ao5": 5,
	"Ao12": 12,
}

def scramble(cube, amount):
	response = subprocess.run(['java', '-jar', 'tnoodle-cli-1.0.0.jar', 'scramble', '-p', str(cube), '-c', str(amount)], capture_output=True).stdout
	response = str(response)
	print(response)
	if cube != "sq1":
		response_clean = response.split('\"')
	else:
		response_clean = response.split("\'")
	print(response_clean)
	scrambles = response_clean[1].split("\\n")
	del scrambles[-1]
	print(scrambles)
	scrambles_formatted = ""
	if cube != "mega":
		for i in range(len(scrambles)):
			scrambles_formatted += f"{str(i+1)}: {scrambles[i]}"
			if not i == len(scrambles):
				scrambles_formatted += str("\n")
	else:
		for i in range(len(scrambles)):
			if (i+1) % 7 == 1 or i == 0:
				scrambles_formatted += f"{str(int((i)/7)+1)}: {scrambles[i]}"
			else:
				scrambles_formatted += scrambles[i]
			if not i == len(scrambles):
				scrambles_formatted += str("\n")
	
	return scrambles_formatted


@client.event
async def on_ready():
    print(f"Bot online as {client.user.name}.")
    await tree.sync()
    print("synced commands")

@tree.command(name="info", description="About the bot")
async def command_info(interaction):
	await interaction.response.send_message("This bot was made to automate daily scrambles in the DannyHTv discord server. It was made and hosted by Digipr01. For any questions and suggestions, you can DM him.")

@tree.command(name="terminate", description="Shuts off the bot")
async def command_shutdown(interaction):
	await interaction.response.send_message("Shutting down DannyHTV bot")
	os._exit(os.EX_OK)
	

@tree.command(name="2x2", description="Generates 2x2 scrambles.")
@app_commands.describe(amount="How many cubes do you want scrambled?")
async def command_2x2(interaction, amount: typing.Literal["Single", "Mo3", "Ao5"] = "Single"):
	await interaction.response.send_message(scramble("two", AverageTypes[amount]))

@tree.command(name="3x3", description="Generates 3x3 scrambles.")
@app_commands.describe(amount="How many cubes do you want scrambled?")
async def command_3x3(interaction, amount: typing.Literal["Single", "Mo3", "Ao5"] = "Single"):
	await interaction.response.send_message(scramble("three", AverageTypes[amount]))

@tree.command(name="4x4", description="Generates 4x4 scrambles.")
@app_commands.describe(amount="How many cubes do you want scrambled?")
async def command_4x4(interaction, amount: typing.Literal["Single", "Mo3", "Ao5"] = "Single"):
	await interaction.response.send_message(scramble("four_fast", AverageTypes[amount]))

@tree.command(name="5x5", description="Generates 5x5 scrambles.")
@app_commands.describe(amount="How many cubes do you want scrambled?")
async def command_5x5(interaction, amount: typing.Literal["Single", "Mo3", "Ao5"] = "Single"):
	await interaction.response.send_message(scramble("five", AverageTypes[amount]))

@tree.command(name="6x6", description="Generates 6x6 scrambles.")
@app_commands.describe(amount="How many cubes do you want scrambled?")
async def command_6x6(interaction, amount: typing.Literal["Single", "Mo3", "Ao5"] = "Single"):
	await interaction.response.send_message(scramble("six", AverageTypes[amount]))
	
@tree.command(name="7x7", description="Generates 7x7 scrambles.")
@app_commands.describe(amount="How many cubes do you want scrambled?")
async def command_7x7(interaction, amount: typing.Literal["Single", "Mo3", "Ao5"] = "Single"):
	await interaction.response.send_message(scramble("seven", AverageTypes[amount]))

@tree.command(name="skewb", description="Generates skewb scrambles.")
@app_commands.describe(amount="How many cubes do you want scrambled?")
async def command_skewb(interaction, amount: typing.Literal["Single", "Mo3", "Ao5"] = "Single"):
	await interaction.response.send_message(scramble("skewb", AverageTypes[amount]))

@tree.command(name="megaminx", description="Generates megaminx scrambles.")
@app_commands.describe(amount="How many cubes do you want scrambled?")
async def command_megaminx(interaction, amount: typing.Literal["Single", "Mo3", "Ao5"] = "Single"):
	await interaction.response.send_message(scramble("mega", AverageTypes[amount]))

@tree.command(name="pyraminx", description="Generates pyraminx scrambles.")
@app_commands.describe(amount="How many cubes do you want scrambled?")
async def command_pyraminx(interaction, amount: typing.Literal["Single", "Mo3", "Ao5"] = "Single"):
	await interaction.response.send_message(scramble("pyra", AverageTypes[amount]))

@tree.command(name="square-1", description="Generates square-1 scrambles.")
@app_commands.describe(amount="How many cubes do you want scrambled?")
async def command_square_1(interaction, amount: typing.Literal["Single", "Mo3", "Ao5"] = "Single"):
	print(amount)
	await interaction.response.send_message(scramble("sq1", AverageTypes[amount]))

	
token = parseToken()
client.run(token)
