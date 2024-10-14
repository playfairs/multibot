import discord
from discord.ext import commands
import json
import os
import sys

print("Python executable:", sys.executable)

# Load config.json for bot settings
with open('config.json') as config_file:
    config = json.load(config_file)

# Enable all intents
intents = discord.Intents.all()

# Initialize the bot and disable the default help command
bot = commands.Bot(command_prefix=config["prefix"], intents=intents, help_command=None)

# Replace this with your actual log channel ID where join/leave messages will be sent
joins_log_channel_id = 123456789012345678  # Replace with your actual log channel ID

@bot.command(name="status")
async def set_custom_status(ctx, *, status: str):
    """Set the bot's custom status (activity)."""
    allowed_user_id = 123456789012345678  # Replace with your actual allowed user ID
    
    if ctx.author.id != allowed_user_id:
        await ctx.send("You must be the owner of this bot to use this command.")
        return
    
    try:
        await bot.change_presence(activity=discord.CustomActivity(name=status))
        await ctx.send(f"Custom status changed to: {status}")
    except Exception as e:
        await ctx.send(f"Failed to change custom status: {e}")

# Event when the bot is ready
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py') and filename != '__init__.py':
            await bot.load_extension(f'cogs.{filename[:-3]}')
            print(f'Loaded Cog: {filename[:-3]}')

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands successfully.")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

    print("Bot is ready and connected.")

# Event for when a member joins the server
@bot.event
async def on_member_join(member):
    # Fetch the log channel using the predefined channel ID
    channel = bot.get_channel(joins_log_channel_id)
    
    # Ensure the channel exists
    if channel:
        await channel.send(f"{member.mention} Welcome! 😊 If you're able to, invite some of your friends! Also, if you want pic perms, rep /vanity in your status.") # Replace /vanity with your actual server vanity if any

# Event for when a member leaves the server
@bot.event
async def on_member_remove(member):
    # Fetch the log channel using the predefined channel ID
    channel = bot.get_channel(joins_log_channel_id)
    
    # Ensure the channel exists
    if channel:
        await channel.send(f"Damn {member.mention} left, they probably won't be back.")

@bot.command()
async def set_log_channel(ctx, channel: discord.TextChannel):
    """Command to set the log channel for join/leave messages."""
    global joins_log_channel_id
    joins_log_channel_id = channel.id
    await ctx.send(f'Log channel set to: {channel.mention}')

# Run the bot
bot.run(config["token"])
