import discord
from discord.ext import commands, tasks
from discord import app_commands
import json
import os

class Pic(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.GUILD_ID = 961097369817071626  # Replace with your actual guild ID
        self.ROLE_ID = 1293380613893656690  # Replace with your actual "pic" role ID
        self.log_channel_id = 1286944011671830559  # Replace with your actual log channel ID
        self.config_file = os.path.join(os.path.dirname(__file__), 'vanity_config.json')
        self.vanity = self.load_vanity()

        # The task is not started automatically, will be managed by commands
        self.check_online_status_task = None

    def load_vanity(self):
        """Load the vanity setting from the config file."""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                config = json.load(f)
                return config.get('vanity', '/default')
        else:
            return '/default'

    def save_vanity(self):
        """Save the current vanity setting to the config file."""
        config = {'vanity': self.vanity}
        with open(self.config_file, 'w') as f:
            json.dump(config, f, indent=4)

    @commands.command(name="vanity")
    async def update_vanity(self, ctx, new_vanity: str):
        """Update the vanity link stored in the config file."""
        # Update the vanity value
        self.vanity = new_vanity
        self.save_vanity()
        
        # Message to acknowledge the update
        await ctx.send(f"Updated vanity to: `{new_vanity}`\n\nRep `{new_vanity}` for pic perms!") 

    @app_commands.command(name="scan", description="Manage scan task for checking vanity in user statuses.")
    async def scan(self, interaction: discord.Interaction):
        """Placeholder command for the /scan command group."""
        await interaction.response.send_message("Use `/scan on` or `/scan off` to control the scan task.")

    @app_commands.command(name="on", description="Start the automatic scanning for vanity in user statuses.")
    async def scan_on(self, interaction: discord.Interaction):
        """Start the automatic scan task."""
        if not self.check_online_status.is_running():
            self.check_online_status.start()
            await interaction.response.send_message("Started the automatic vanity status scan.")
        else:
            await interaction.response.send_message("The scan is already running.")

    @app_commands.command(name="off", description="Stop the automatic scanning for vanity in user statuses.")
    async def scan_off(self, interaction: discord.Interaction):
        """Stop the automatic scan task."""
        if self.check_online_status.is_running():
            self.check_online_status.stop()
            await interaction.response.send_message("Stopped the automatic vanity status scan.")
        else:
            await interaction.response.send_message("The scan is not currently running.")

    # Status check task (does not start automatically)
    @tasks.loop(seconds=10)
    async def check_online_status(self):
        await self.deep_scan_role_check()

    # Deep scan command to manually check all users
    @app_commands.command(name="deep_scan", description="Manually check all users for vanity link in status.")
    async def deep_scan(self, interaction: discord.Interaction):
        result_message = await self.deep_scan_role_check()
        await interaction.response.send_message(result_message)

    # Helper function to perform the deep scan and role adjustment
    async def deep_scan_role_check(self):
        guild = self.bot.get_guild(self.GUILD_ID)
        if guild is None:
            print(f"Guild not found with ID: {self.GUILD_ID}")
            return "Guild not found."

        await guild.chunk()  # Ensure all members are cached

        role = guild.get_role(self.ROLE_ID)
        if role is None:
            print(f"Role not found with ID: {self.ROLE_ID}")
            return "Role with the specified ID not found."

        log_channel = guild.get_channel(self.log_channel_id)
        if log_channel is None:
            print(f"Log channel not found with ID: {self.log_channel_id}")
            return "Log channel not found."

        users_with_vanity = []
        users_without_vanity = []

        # Check all members and adjust roles
        for member in guild.members:
            has_vanity = False
            if member.raw_status in ['online', 'idle', 'dnd']:
                if member.activity and isinstance(member.activity, discord.CustomActivity):
                    # Check if the member has the updated vanity link in their status
                    if self.vanity in member.activity.name:
                        has_vanity = True
                        users_with_vanity.append(member)

            # Adjust roles based on presence of the vanity link
            if has_vanity and role not in member.roles:
                try:
                    await member.add_roles(role)
                    await log_channel.send(f"Gave pic perms to {member.mention}, user has '{self.vanity}' in status")
                except discord.Forbidden:
                    print(f"Bot doesn't have permission to assign roles to {member.name}")
                except discord.HTTPException as e:
                    print(f"Failed to assign role due to HTTPException: {e}")

            # If user had the vanity but now does not, remove role
            elif not has_vanity and role in member.roles:
                if member.raw_status != 'offline':
                    try:
                        await member.remove_roles(role)
                        await log_channel.send(f"Removed pic perms from {member.mention}, user no longer has '{self.vanity}' in status")
                    except discord.Forbidden:
                        print(f"Bot doesn't have permission to remove roles from {member.name}")
                    except discord.HTTPException as e:
                        print(f"Failed to remove role due to HTTPException: {e}")
                    users_without_vanity.append(member)
                else:
                    print(f"Skipping removal for {member.name} (offline but previously had '{self.vanity}').")

        print(f"Deep scan complete: {len(users_with_vanity)} users have '{self.vanity}' in their status.")
        return (f"Deep scan complete. {len(users_with_vanity)} users have '{self.vanity}' in their status, "
                f"{len(users_without_vanity)} users had the role removed.")

# Event listener for on_message to respond to "pic perms" requests
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return  # Prevent bot from replying to itself

        # Convert the message to lowercase for easier matching
        content = message.content.lower()

        # Check for variations of asking for "pic perms"
        if any(keyword in content for keyword in ["get pic perms", "give me pic", "give me pic perms", "how do i get pic perms", "pic perms"]):
            await message.channel.send(f"Rep `{self.vanity}` in status for pic perms, or boost the server!")

async def setup(bot):
    await bot.add_cog(Pic(bot))
