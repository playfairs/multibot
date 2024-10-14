import discord
from discord.ext import commands

class EmbedResponse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.lower() == "Keyword" and not message.author.bot:
            video_path = "C:\\Users\\user\\path\\filename.mp4" # Replace with your actual file path, also make sure their \\ not \ for the bot to read them as a path
            await message.channel.send(file=discord.File(video_path))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.lower() == "keyword" and not message.author.bot:
            video_path = "C:\\Users\\user\\path\\filename.mp4" # just do the same thing as previously mentioned
            await message.channel.send(file=discord.File(video_path))

async def setup(bot):
    await bot.add_cog(EmbedResponse(bot))
