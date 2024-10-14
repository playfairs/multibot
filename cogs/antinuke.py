import discord
from discord.ext import commands

class AntiNuke(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        # Retrieve the user who modified the channel, if available
        provoker = await self.find_channel_modifier(after.guild)

        # Assuming you want to pass the `provoker` as the target for logging purposes
        if provoker:
            await self.log_action(
                action_type="channel_modify", 
                provoker=provoker, 
                guild=after.guild, 
                description="Channel modification action detected and handled", 
                target=provoker  # Pass the `provoker` user as the target
            )

    async def log_action(self, action_type, provoker, guild, description, target):
        # Create an embed message for logging
        embed = discord.Embed(
            title=f"Action: {action_type}",
            description=description,
            color=discord.Color.red()
        )
        embed.add_field(name="Provoker", value=f"{provoker.name}#{provoker.discriminator}", inline=True)
        embed.add_field(name="Guild", value=guild.name, inline=True)

        # Check if the target is a User or Member object before accessing name and discriminator
        if isinstance(target, (discord.User, discord.Member)):
            embed.add_field(name="Target", value=f"{target.name}#{target.discriminator}", inline=True)
        else:
            embed.add_field(name="Target", value=str(target), inline=True)

        # Send the log message to a specific channel (replace with your logging channel ID)
        logging_channel = guild.get_channel(1292729507807101101)  # Replace with your logging channel ID
        if logging_channel:
            await logging_channel.send(embed=embed)

    async def find_channel_modifier(self, guild):
        # A placeholder function to retrieve the user who modified a channel.
        # You can implement your own logic, such as fetching audit logs.
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_update):
            return entry.user  # Return the user who modified the channel
        return None  # Return None if no user is found

async def setup(bot):
    await bot.add_cog(AntiNuke(bot))
