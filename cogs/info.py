import discord
from discord.ext import commands
from datetime import datetime, timezone


class InfoCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="si", help="Show the server info.")
    async def server_info(self, ctx):
        """Shows the server information in a red embed."""

        # Check if the bot has permission to send embeds
        if not ctx.guild.me.guild_permissions.embed_links:
            await ctx.send("I don't have permission to send embeds!")
            return

        guild = ctx.guild
        owner = guild.owner
        verification_level = guild.verification_level
        boosts = guild.premium_subscription_count
        members = guild.member_count
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        creation_time = guild.created_at.strftime("%B %d, %Y %I:%M %p")

        # Calculate years since creation
        now = datetime.now(timezone.utc)
        created_at = guild.created_at
        delta = now - created_at
        years = delta.days // 365

        # Format the creation time in years (rounded)
        time_since_creation = f"{years} year{'s' if years != 1 else ''} ago"

        # Get the server's icon URL
        server_icon_url = guild.icon.url if guild.icon else None

        # Embed creation
        embed = discord.Embed(
            description=f"{creation_time} ({time_since_creation})",  # Display time since creation in years
            color=discord.Color.red()  # Red color for the embed
        )

        # Set the server icon on the left side
        if server_icon_url:
            embed.set_thumbnail(url=server_icon_url)

        # Add the server name and ID without a link
        embed.title = f"{guild.name} \n`{guild.id}`"

        # Add inline fields for 'Information' and 'Statistics'
        embed.add_field(
            name="**Information**",
            value=(f"> Owner: {owner.mention}\n"
                   f"> Verification: {verification_level}\n"
                   f"> Nitro Boosts: {boosts}"),
            inline=True  # Inline to make it side by side
        )

        embed.add_field(
            name="**Statistics**",
            value=(f"> Members: {members}\n"
                   f"> Text Channels: {text_channels}\n"
                   f"> Voice Channels: {voice_channels}"),
            inline=True  # Inline to make it side by side
        )

        # Footer with requester information
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(InfoCog(bot))
