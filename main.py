import discord
import json

def parseToken():
    with open("configure.json") as read_file:
        file_data = json.load(read_file)
        print(type(file_data))
        return file_data["token"]

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
token = parseToken()
client.run(token)