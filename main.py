import discord
from discord import app_commands
from discord.ext import tasks
import os
import json
import subprocess
import typing
import datetime
import random

def parseToken():
    with open("configure.json") as read_file:
        file_data = json.load(read_file)
        return file_data["token"]

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)
timezone = datetime.timezone(datetime.timedelta(hours=1))

privateGuild = discord.Object(id=1303082498929983549)

#dailyScrambles
scrambleTime = datetime.time(hour=7, minute=00, tzinfo=timezone)
scrambleChannelId = 1322667465372598333
dailyCubes = ["two", "four_fast", "five", "six", "seven", "skewb", "sq1", "mega", "pyra", "three_oh"]
dailyAverages = ["Single", "Mo3", "Ao5"]

@tasks.loop(time=scrambleTime)
async def sendDailyScramble():
	await client.wait_until_ready()
	scrambleChannel = client.get_channel(scrambleChannelId)
	daily3x3Average = random.choice(dailyAverages)
	dailyCube = random.choice(dailyCubes)
	dailyCubeAverage = random.choice(dailyAverages)
	await scrambleChannel.send(embeds=[scramble("three", AverageTypes[daily3x3Average], sender="Daily Scrambler", daily= True), scramble(dailyCube, AverageTypes[dailyCubeAverage], sender="Daily Scrambler", daily= True)])

AverageTypes = {
	"Single": 1,
	"Mo3": 3,
	"Ao5": 5,
	"Ao12": 12,
}

cubeTypes = {
	"two": "2x2",
	"three": "3x3",
	"four": "4x4",
	"four_fast": "4x4",
	"five": "5x5",
	"six": "6x6",
	"seven": "7x7",
	"mega": "megaminx",
	"skewb": "skewb",
	"pyra": "pyraminx",
	"sq1": "square-1",
	"three_ni": "3bld",
	"four_ni": "4bld",
	"five_ni": "5bld",
	"three_fm": "FMC",
	"three_oh": "3x3 one handed",
	"clock": "forbidden circle",
}

def scramble(cube, amount, sender="Unknown peep", daily=False):
	print(f"{sender} has tried to generate {amount} scramble(s) for {cubeTypes[cube]}")
	if not daily:
		scramble_embed = discord.Embed(title=f"Your {cubeTypes[cube]} scramble(s)", color=0xa80000, timestamp=datetime.datetime.now(tz=timezone))
		if cube == "clock":
			scramble_embed.add_field(name="That circle is illegal around here bud", value="We do not like that circle, why you want a circle huh? Cubes are better. \nEnjoy your fake \'cube\' scramble.")
	else:
		if cube == "three":
			scramble_embed = discord.Embed(title=f"Your daily 3x3 scramble(s)", color=0xa80000, timestamp=datetime.datetime.now(tz=timezone))
		else:
			scramble_embed = discord.Embed(title=f"Today\'s extra scramble(s) are... ||{cubeTypes[cube]}||", color=0xa80000, timestamp=datetime.datetime.now(tz=timezone))
	if True:
		if cube != "three_oh":
			scramble_cube = cube
		else:
			scramble_cube = "three"
		response = subprocess.run(['java', '-jar', 'CLI/tnoodle-cli-1.1.0.jar', 'scramble', '-p', str(scramble_cube), '-c', str(amount)], capture_output=True).stdout
		response = str(response)
		if cube != "sq1" and cube != "clock":
			response_clean = response.split('\"')
		else:
			response_clean = response.split("\'")
		scrambles = response_clean[1].split("\\n")
		del scrambles[-1]
		scrambles_formatted = ""
		if cube != "mega":
			for i in range(len(scrambles)):
				scrambles_formatted += f"{str(i+1)}: {scrambles[i]}"
				if not i == len(scrambles):
					scrambles_formatted += str("\n")
				scramble_embed.add_field(name=f"Scramble {i+1}:", value=scrambles[i], inline=False)
		else:
			for i in range(int(len(scrambles)/7)):
				currentScramble = ""
				for j in range(7):
					currentScramble += scrambles[i*7+j]
					if j != 6:
						currentScramble += "\n"
				scrambles_formatted += f"{str(int((i/7)+1))}: {currentScramble}"
				if not i == len(scrambles):
					scrambles_formatted += str("\n")
				scramble_embed.add_field(name=f"Scramble {str(i+1)}:", value=currentScramble, inline=False)
	else:
		scramble_embed.add_field(name="Scrambling Failed", value="There has been an error generating your scrambles, please try again or contact @digipr01", inline=False)
	return scramble_embed


@client.event
async def on_ready():
    print(f"Bot online as {client.user.name}.")
    await tree.sync()
    print("synced commands")
    sendDailyScramble.start()

@tree.command(name="info", description="About the bot")
async def command_info(interaction):
	await interaction.response.send_message("This bot was made to automate daily scrambles in the DannyHTv discord server. It was made and hosted by Digipr01. For any questions and suggestions, you can DM him.")

@tree.command(name="terminate", description="Shuts off the bot")
async def command_shutdown(interaction):
	await interaction.response.send_message("Shutting down DannyHTV bot", ephemeral=True)
	os._exit(os.EX_OK)
	

@tree.command(name="2x2", description="Generates 2x2 scrambles.")
@app_commands.describe(amount="How many cubes do you want scrambled?")
async def command_2x2(interaction, amount: typing.Literal["Single", "Mo3", "Ao5"] = "Single"):
	await interaction.response.send_message("Generating scrambles, give me a second")
	await interaction.edit_original_response(content=None, embed=scramble("two", AverageTypes[amount], sender=interaction.user))

@tree.command(name="3x3", description="Generates 3x3 scrambles.")
@app_commands.describe(amount="How many cubes do you want scrambled?")
async def command_3x3(interaction, amount: typing.Literal["Single", "Mo3", "Ao5"] = "Single"):
	await interaction.response.send_message("Generating scrambles, give me a second")
	await interaction.edit_original_response(content=None, embed=scramble("three", AverageTypes[amount], sender=interaction.user))

@tree.command(name="4x4", description="Generates 4x4 scrambles.")
@app_commands.describe(amount="How many cubes do you want scrambled?")
async def command_4x4(interaction, amount: typing.Literal["Single", "Mo3", "Ao5"] = "Single"):
	await interaction.response.send_message("Generating scrambles, give me a second")
	await interaction.edit_original_response(content=None, embed=scramble("four_fast", AverageTypes[amount], sender=interaction.user))

@tree.command(name="5x5", description="Generates 5x5 scrambles.")
@app_commands.describe(amount="How many cubes do you want scrambled?")
async def command_5x5(interaction, amount: typing.Literal["Single", "Mo3", "Ao5"] = "Single"):
	await interaction.response.send_message("Generating scrambles, give me a second")
	await interaction.edit_original_response(content=None, embed=scramble("five", AverageTypes[amount], sender=interaction.user))

@tree.command(name="6x6", description="Generates 6x6 scrambles.")
@app_commands.describe(amount="How many cubes do you want scrambled?")
async def command_6x6(interaction, amount: typing.Literal["Single", "Mo3", "Ao5"] = "Single"):
	await interaction.response.send_message("Generating scrambles, give me a second")
	await interaction.edit_original_response(content=None, embed=scramble("six", AverageTypes[amount], sender=interaction.user))
	
@tree.command(name="7x7", description="Generates 7x7 scrambles.")
@app_commands.describe(amount="How many cubes do you want scrambled?")
async def command_7x7(interaction, amount: typing.Literal["Single", "Mo3", "Ao5"] = "Single"):
	await interaction.response.send_message("Generating scrambles, give me a second")
	await interaction.edit_original_response(content=None, embed=scramble("seven", AverageTypes[amount], sender=interaction.user))

@tree.command(name="skewb", description="Generates skewb scrambles.")
@app_commands.describe(amount="How many cubes do you want scrambled?")
async def command_skewb(interaction, amount: typing.Literal["Single", "Mo3", "Ao5"] = "Single"):
	await interaction.response.send_message("Generating scrambles, give me a second")
	await interaction.edit_original_response(content=None, embed=scramble("skewb", AverageTypes[amount], sender=interaction.user))

@tree.command(name="megaminx", description="Generates megaminx scrambles.")
@app_commands.describe(amount="How many cubes do you want scrambled?")
async def command_megaminx(interaction, amount: typing.Literal["Single", "Mo3", "Ao5"] = "Single"):
	await interaction.response.send_message("Generating scrambles, give me a second")
	await interaction.edit_original_response(content=None, embed=scramble("mega", AverageTypes[amount], sender=interaction.user))

@tree.command(name="pyraminx", description="Generates pyraminx scrambles.")
@app_commands.describe(amount="How many cubes do you want scrambled?")
async def command_pyraminx(interaction, amount: typing.Literal["Single", "Mo3", "Ao5"] = "Single"):
	await interaction.response.send_message("Generating scrambles, give me a second")
	await interaction.edit_original_response(content=None, embed=scramble("pyra", AverageTypes[amount], sender=interaction.user))

@tree.command(name="square-1", description="Generates square-1 scrambles.")
@app_commands.describe(amount="How many cubes do you want scrambled?")
async def command_square_1(interaction, amount: typing.Literal["Single", "Mo3", "Ao5"] = "Single"):
	await interaction.response.send_message("Generating scrambles, give me a second")
	await interaction.edit_original_response(content=None, embed=scramble("sq1", AverageTypes[amount], sender=interaction.user))

@tree.command(name="3x3-blindfolded", description="Generates 3x3-blindfolded scrambles.")
@app_commands.describe(amount="How many cubes do you want scrambled?")
async def command_3bld(interaction, amount: typing.Literal["Single", "Mo3"] = "Single"):
	await interaction.response.send_message("Generating scrambles, give me a second")
	await interaction.edit_original_response(content=None, embed=scramble("three_ni", AverageTypes[amount], sender=interaction.user))
	
@tree.command(name="4x4-blindfolded", description="Generates 4x4-blindfolded scrambles.")
@app_commands.describe(amount="How many cubes do you want scrambled?")
async def command_4bld(interaction, amount: typing.Literal["Single", "Mo3"] = "Single"):
	await interaction.response.send_message("Generating scrambles, give me a second")
	await interaction.edit_original_response(content=None, embed=scramble("four_ni", AverageTypes[amount], sender=interaction.user))
	
@tree.command(name="5x5-blindfolded", description="Generates 5x5-blindfolded scrambles.")
@app_commands.describe(amount="How many cubes do you want scrambled?")
async def command_5bld(interaction, amount: typing.Literal["Single", "Mo3"] = "Single"):
	await interaction.response.send_message("Generating scrambles, give me a second")
	await interaction.edit_original_response(content=None, embed=scramble("five_ni", AverageTypes[amount], sender=interaction.user))
	
@tree.command(name="fmc", description="Generates scrambles for the 3x3 fewest move challenge.")
async def command_fmc(interaction):
	await interaction.response.send_message("Generating scrambles, give me a second")
	await interaction.edit_original_response(content=None, embed=scramble("three_fm", 1, sender=interaction.user))
	
@tree.command(name="clock", description="Generates clock scrambles. (ew)")
@app_commands.describe(amount="How many cubes do you want scrambled?")
async def command_clock(interaction, amount: typing.Literal["Single", "Mo3", "Ao5"] = "Single"):
	await interaction.response.send_message("Generating scrambles, give me a second")
	await interaction.edit_original_response(content=None, embed=scramble("clock", AverageTypes[amount], sender=interaction.user))

@tree.command(name="3x3-one-handed", description="Generates 3x3 scrambles for one handed solving.")
@app_commands.describe(amount="How many cubes do you want scrambled?")
async def command_3x3OH(interaction, amount: typing.Literal["Single", "Mo3", "Ao5"] = "Single"):
	await interaction.response.send_message("Generating scrambles, give me a second")
	await interaction.edit_original_response(content=None, embed=scramble("three_oh", AverageTypes[amount], sender=interaction.user))


token = parseToken()
client.run(token)
