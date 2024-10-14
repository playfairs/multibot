import discord
from discord.ext import commands

class SuicideResponder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Sets of keywords to trigger the responses
        self.keywords_kms = ["kms", "kill myself", "im gonna kms", "end it all"]
        self.keywords_kys = ["kys", "kill yourself", "die"]

    @commands.Cog.listener()
    async def on_message(self, message):
        # Don't respond to bots or if the message is from the bot itself
        if message.author.bot:
            return
        
        # Check if the message contains any of the "kms" keywords (case-insensitive)
        if any(keyword.lower() in message.content.lower() for keyword in self.keywords_kms):
            # Create a DM message for "kms" related keywords
            dm_message_kms = (
                "Hey, I heard you said 'kms', if you do need someone to talk to you have <@785042666475225109> and <@1256856675520876696>, they both are here for you nobody hates you, even if you think the world hates you, you're purfect don't think about anyone else's opinions"
            )
            try:
                # Send a direct message to the user
                await message.author.send(dm_message_kms)
            except discord.Forbidden:
                # If the bot cannot send a DM, log the error (optional)
                print(f"Could not send DM to {message.author.name}")

        # Check if the message contains any of the "kys" keywords (case-insensitive)
        elif any(keyword.lower() in message.content.lower() for keyword in self.keywords_kys):
            # Create a DM message for "kys" related keywords
            dm_message_kys = (
                "I noticed you said something related to KYS, that was not very gigachad sigma grindset skibidi ohio rizz of you. "
                "There are people who are very suicidal and you would only be controlling the population.. wait, i mean you would only be encouraging population control.. wait"
                "i mean you are a very not sigma person for telling someone to kill themself, you should kill yourself!"
                "**This message is sponsored by [NordVPN](https://nordvpn.com)!**"
            )
            try:
                # Send a direct message to the user
                await message.author.send(dm_message_kys)
            except discord.Forbidden:
                # If the bot cannot send a DM, log the error (optional)
                print(f"Could not send DM to {message.author.name}")

async def setup(bot):
    await bot.add_cog(SuicideResponder(bot))
