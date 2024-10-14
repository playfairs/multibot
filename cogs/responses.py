import discord
from discord.ext import commands
import random

class Responses(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.responses = {
            "Trigger 1": [
                "Response 1",
                "Response 2",
                "Response 3"
                # Add more as needed
            ],
            "Trigger 2": [
                "Response 1",
                "Response 2",
                "Response 3"
                # Again add more as needed
            ]
        }

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return  # Ignore messages from the bot itself

        # Get a random response based on the message content
        for trigger, responses in self.responses.items():
            if trigger in message.content.lower():
                response = random.choice(responses)
                await message.channel.send(response)
                break  # Stop checking after the first match

# Setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(Responses(bot))
