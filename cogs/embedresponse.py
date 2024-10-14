import discord
from discord.ext import commands

class EmbedResponse(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.lower() == "nuh uh" and not message.author.bot:
            video_path = "C:\\Users\\fnafl\\Downloads\\heresy-main\\heresy-main\\nuhuh.mp4"
            await message.channel.send(file=discord.File(video_path))

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.lower() == "minion tampons" and not message.author.bot:
            video_path = "C:\\Users\\fnafl\\Downloads\\heresy-main\\heresy-main\\miniontampons.mov"
            await message.channel.send(file=discord.File(video_path))

async def setup(bot):
    await bot.add_cog(EmbedResponse(bot))
