import discord
from discord import app_commands
from discord.ext import commands
import sqlite3
import time
import aiohttp  # Import aiohttp for HTTP requests

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()  # Create a session for HTTP requests
        self.initialize_db()
        print("[Utility] Initialized Utility cog and database connection.")

    def initialize_db(self):
        """Initialize the database to store AFK users."""
        try:
            conn = sqlite3.connect('afk_users.db')
            cursor = conn.cursor()
            cursor.execute('''CREATE TABLE IF NOT EXISTS afk_users (
                user_id INTEGER PRIMARY KEY,
                reason TEXT,
                afk_time INTEGER
            )''')
            conn.commit()
            conn.close()
            print("[Utility] Database initialized successfully.")
        except sqlite3.Error as e:
            print(f"[Utility] Error initializing database: {e}")

    def set_afk(self, user_id, reason):
        """Sets the AFK status for a user with the current timestamp."""
        try:
            conn = sqlite3.connect('afk_users.db')
            cursor = conn.cursor()
            cursor.execute('''INSERT OR REPLACE INTO afk_users (user_id, reason, afk_time)
            VALUES (?, ?, ?)''', (user_id, reason, int(time.time())))
            conn.commit()
            conn.close()
            print(f"[Utility] AFK set for user {user_id} with reason: {reason}")
        except sqlite3.Error as e:
            print(f"[Utility] Error setting AFK: {e}")

    def get_afk_status(self, user_id):
        """Gets the AFK status and timestamp for a user."""
        try:
            conn = sqlite3.connect('afk_users.db')
            cursor = conn.cursor()
            cursor.execute('''SELECT reason, afk_time FROM afk_users WHERE user_id = ?''', (user_id,))
            result = cursor.fetchone()
            conn.close()
            return result
        except sqlite3.Error as e:
            print(f"[Utility] Error getting AFK status: {e}")
            return None

    def remove_afk(self, user_id):
        """Removes the AFK status for a user."""
        try:
            conn = sqlite3.connect('afk_users.db')
            cursor = conn.cursor()
            cursor.execute('''DELETE FROM afk_users WHERE user_id = ?''', (user_id,))
            conn.commit()
            conn.close()
            print(f"[Utility] AFK removed for user {user_id}.")
        except sqlite3.Error as e:
            print(f"[Utility] Error removing AFK: {e}")

    def format_time_ago(self, afk_time):
        """Formats the time since the AFK status was set."""
        time_elapsed = int(time.time()) - afk_time
        if time_elapsed < 60:
            return "a few seconds ago"
        elif time_elapsed < 3600:  # Less than 1 hour
            minutes = time_elapsed // 60
            return f"{minutes} minutes ago"
        elif time_elapsed < 86400:  # Less than 24 hours
            hours = time_elapsed // 3600
            return f"{hours} hours ago"
        else:
            days = time_elapsed // 86400
            return f"{days} days ago"

    @app_commands.command(name="ping", description="Check the bot's latency")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.send_message(f'Pong! {round(self.bot.latency * 1000)}ms', ephemeral=True)

    @app_commands.command(name="userinfo", description="Get information about a user")
    async def userinfo(self, interaction: discord.Interaction, member: discord.Member = None):
        member = member or interaction.user
        embed = discord.Embed(title=f"{member}'s Info", color=discord.Color.blue())
        embed.add_field(name="ID", value=member.id)
        embed.add_field(name="Name", value=member.name)
        embed.add_field(name="Created At", value=member.created_at.strftime("%m/%d/%Y, %H:%M:%S"))
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @commands.command(name="av", help="Show your avatar.")
    async def avatar(self, ctx, member: discord.Member = None):
        """Displays the avatar of the specified user or yourself if no one is mentioned."""
        member = member or ctx.author
        embed = discord.Embed(title=f"{member.name}'s Avatar", color=discord.Color.blue())
        embed.set_image(url=member.avatar.url)
        embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
        await ctx.send(embed=embed)

    @commands.command(name="banner", help="Show your banner.")
    async def banner(self, ctx, member: discord.Member = None):
        """Displays the banner of the specified user or yourself if no one is mentioned."""
        member = member or ctx.author

        # Fetch the member from the guild to ensure we're getting updated information
        member = ctx.guild.get_member(member.id) or member  # Fallback to the original member

        # Check if the member has a banner
        if member.banner:
            embed = discord.Embed(title=f"{member.name}'s Banner", color=discord.Color.blue())
            embed.set_image(url=member.banner.url)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{member.mention} does not have a banner (probably too poor to have nitro for a banner)")

    @commands.command(name="sav", help="Show your server avatar.")
    async def sav(self, ctx, member: discord.Member = None):
        """Displays the server avatar of the specified user or yourself if no one is mentioned."""
        member = member or ctx.author

        # Check if the member has a server avatar
        if member.guild_avatar:  # Check for the guild avatar specifically
            embed = discord.Embed(title=f"{member.name}'s Server Avatar", color=discord.Color.blue())
            embed.set_image(url=member.guild_avatar.url)
            embed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
        else:
            await ctx.send(f"{member.mention} does not have a server avatar.")

    # New print command
    @commands.command(name="print", description="Make the bot say the message you provide and delete your command.")
    async def print_command(self, ctx, *, message: str):
        """Print the provided message through the bot and delete the command message."""
        await ctx.message.delete()  # Deletes the user's command message instantly
        await ctx.send(message)  # Bot sends the provided message

    # New change avatar command
    @commands.command(name="changeav", description="Change the bot's avatar to a provided URL.")
    async def change_avatar(self, ctx, url: str):
        """Change the bot's avatar to the provided URL. Restricted to the bot owner."""
        OWNER_ID = 123456789012345678  # Replace with your actual Discord User ID

        # Check if the user is the bot owner
        if ctx.author.id != OWNER_ID:
            await ctx.send("You are not authorized to use this command.", delete_after=5)
            return

        # Use aiohttp to fetch the image from the URL
        async with ctx.typing():
            try:
                async with self.session.get(url) as response:
                    if response.status == 200:
                        avatar_data = await response.read()
                        await self.bot.user.edit(avatar=avatar_data)
                        await ctx.send("Successfully updated the bot's avatar.", delete_after=5)
                    else:
                        await ctx.send("Failed to fetch the image from the provided URL.", delete_after=5)
            except Exception as e:
                await ctx.send(f"An error occurred: {e}", delete_after=5)

    # AFK Commands
    @commands.command(name='afk')
    async def afk(self, ctx, *, reason: str = "AFK"):
        """Set the AFK status with an optional reason."""
        user_id = ctx.author.id
        self.set_afk(user_id, reason)

        embed = discord.Embed(
            description=f"✔ {ctx.author.display_name}, you're now AFK with the status: **{reason}**.",
            color=discord.Color.blue()
        )
        await ctx.reply(embed=embed, mention_author=True)

    @commands.Cog.listener()
    async def on_message(self, message):
        # Ignore bot messages or messages that don't originate from a user
        if message.author.bot or message.webhook_id is not None:
            return

        # Check if the message is a command and ignore it
        ctx = await self.bot.get_context(message)
        if ctx.valid:
            print(f"[Debug] Ignoring AFK removal for command: {message.content}")
            return

        # Check if the author is AFK
        afk_data = self.get_afk_status(message.author.id)
        
        if afk_data:
            print(f"[Debug] Removing AFK for user: {message.author.id} due to manual message.")
            self.remove_afk(message.author.id)

            embed = discord.Embed(
                description=f"👋 Welcome back, {message.author.display_name}! You were AFK for {self.format_time_ago(afk_data[1])}.",
                color=discord.Color.green()
            )
            await message.channel.send(embed=embed)

        # Check for mentioned users who are AFK and notify the sender
        for mentioned_user in message.mentions:
            afk_data = self.get_afk_status(mentioned_user.id)
            if afk_data:
                embed = discord.Embed(
                    description=f"{mentioned_user.display_name} is currently AFK: **{afk_data[0]}**.",
                    color=discord.Color.red()
                )
                await message.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        # Check if the author is AFK and notify if they edit their message
        afk_data = self.get_afk_status(before.author.id)
        if afk_data:
            embed = discord.Embed(
                description=f"{before.author.display_name} is currently AFK: **{afk_data[0]}**.",
                color=discord.Color.red()
            )
            await after.channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        # Notify when a user's AFK status is mentioned
        if message.author.bot:
            return
        
        afk_data = self.get_afk_status(message.author.id)
        if afk_data:
            embed = discord.Embed(
                description=f"{message.author.display_name} was AFK: **{afk_data[0]}**.",
                color=discord.Color.red()
            )
            await message.channel.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Utility(bot))
