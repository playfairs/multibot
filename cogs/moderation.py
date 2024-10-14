import discord
from discord.ext import commands
import os

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='ban', help='Bans a member by User ID or mention.')
    async def ban(self, ctx, member: discord.Member = None, user_id: int = None):
        if member is None and user_id is None:
            await ctx.send("You must specify a user to ban (mention or User ID).")
            return
        
        # If the member is not provided, fetch using user_id
        if member is None:
            try:
                member = await ctx.guild.fetch_member(user_id)
            except discord.NotFound:
                await ctx.send("User not found.")
                return

        try:
            await member.ban(reason=f"Banned by {ctx.author}")
            await ctx.message.add_reaction('👍')
            await ctx.send(f"{member} has been banned.")
        except discord.Forbidden:
            await ctx.send("I do not have permission to ban this user.")
        except discord.HTTPException:
            await ctx.send("Failed to ban the user.")

    @commands.command(name='unban', help='Unbans a member by User ID.')
    async def unban(self, ctx, user_id: int):
        guild = ctx.guild
        banned_users = await guild.bans()

        user = discord.Object(id=user_id)
        try:
            await guild.unban(user)
            await ctx.message.add_reaction('👍')
            await ctx.send(f"User with ID {user_id} has been unbanned.")
        except discord.NotFound:
            await ctx.send("User not found in the ban list.")
        except discord.Forbidden:
            await ctx.send("I do not have permission to unban this user.")
        except discord.HTTPException:
            await ctx.send("Failed to unban the user.")

    @commands.command(name='kick', help='Kicks a member by User ID or mention.')
    async def kick(self, ctx, member: discord.Member = None, user_id: int = None):
        if member is None and user_id is None:
            await ctx.send("You must specify a user to kick (mention or User ID).")
            return
        
        if member is None:
            try:
                member = await ctx.guild.fetch_member(user_id)
            except discord.NotFound:
                await ctx.send("User not found.")
                return

        try:
            await member.kick(reason=f"Kicked by {ctx.author}")
            await ctx.message.add_reaction('👍')
            await ctx.send(f"{member.mention} has been kicked.")
        except discord.Forbidden:
            await ctx.send("I do not have permission to kick this user.")
        except discord.HTTPException:
            await ctx.send("Failed to kick the user.")

    @commands.command(name='warn', help='Warns a member by User ID or mention.')
    async def warn(self, ctx, member: discord.Member = None, user_id: int = None):
        if member is None and user_id is None:
            await ctx.send("You must specify a user to warn (mention or User ID).")
            return
        
        if member is None:
            try:
                member = await ctx.guild.fetch_member(user_id)
            except discord.NotFound:
                await ctx.send("User not found.")
                return
        
        # Create directory if it doesn't exist
        log_dir = "Warn Logs"
        os.makedirs(log_dir, exist_ok=True)

        # Log the warning
        with open(os.path.join(log_dir, f"{member.name}.txt"), 'a') as f:
            f.write(f"Warned by {ctx.author}: {ctx.message.content}\n")

        await ctx.send(f"{member} has been warned.")
    
    @commands.command(name='to', help='Times out a member for a specified duration (default is 1 minute).')
    async def timeout(self, ctx, member: discord.Member = None, user_id: int = None, seconds: int = 60):
        if member is None and user_id is None:
            await ctx.send("You must specify a user to timeout (mention or User ID).")
            return
        
        if member is None:
            try:
                member = await ctx.guild.fetch_member(user_id)
            except discord.NotFound:
                await ctx.send("User not found.")
                return
        
        # Set timeout for the specified duration
        try:
            await member.timeout(discord.utils.utcnow() + discord.timedelta(seconds=seconds), reason=f"Timed out by {ctx.author}")
            await ctx.message.add_reaction('✅')
            await ctx.send(f"{member} has been timed out for {seconds} seconds.")
        except discord.Forbidden:
            await ctx.send("I do not have permission to timeout this user.")
        except discord.HTTPException:
            await ctx.send("Failed to timeout the user.")

    @commands.command(name='uto', help='Removes the timeout from a member by User ID or mention.')
    async def remove_timeout(self, ctx, member: discord.Member = None, user_id: int = None):
        if member is None and user_id is None:
            await ctx.send("You must specify a user to remove timeout (mention or User ID).")
            return
        
        if member is None:
            try:
                member = await ctx.guild.fetch_member(user_id)
            except discord.NotFound:
                await ctx.send("User not found.")
                return
        
        try:
            await member.timeout(None, reason=f"Timeout removed by {ctx.author}")
            await ctx.message.add_reaction('✅')
            await ctx.send(f"Timeout has been removed from {member}.")
        except discord.Forbidden:
            await ctx.send("I do not have permission to remove timeout from this user.")
        except discord.HTTPException:
            await ctx.send("Failed to remove timeout from the user.")

async def setup(bot):
    await bot.add_cog(Moderation(bot))
