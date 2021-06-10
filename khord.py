import discord 

class KhordClient(discord.Client):
    async def on_ready(self):
        print('Logged in as {0.user}'.format(client))

    async def on_message(self, message):
        message.content = message.content.lower()
        if message.author == client.user or not message.content.startswith(";"):
            return
        else:
            if message.content.startswith(";hello"):
                await message.channel.send("Hello, mortal.")


client = KhordClient()
client.run("key")