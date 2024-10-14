import discord
from discord.ext import commands

class HelpCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help', description="Shows the command menu or details about a specific command.")
    async def help_command(self, ctx, command_name: str = None):
        if command_name is None:
            # Create the main embed with a blue color
            embed = discord.Embed(
                title="Heresy Command Menu",  # Title of the embed
                description="Information\n > [] = optional, <> = required",
                color=discord.Color.blue()  # Embed color set to blue
            )

            # Set the bot's avatar as the embed thumbnail
            embed.set_thumbnail(url=self.bot.user.avatar.url)

            # Add a field for inviting the bot
            embed.add_field(name="Invite", value="[Invite](https://youtu.be/dQw4w9WgXcQ?si=k6AKXJWW4BW7GmBQ)", inline=False)

            # Change the footer to reflect the dropdown menu instruction
            embed.set_footer(text="Select a category from the dropdown menu below")

            # Create the dropdown menu options (with Utility combined)
            options = [
                discord.SelectOption(label="Alphabet"),
                discord.SelectOption(label="Application"),
                discord.SelectOption(label="IDLogger"),
                discord.SelectOption(label="IDToTokenCog"),
                discord.SelectOption(label="MessageLogger"),
                discord.SelectOption(label="Mirror"),
                discord.SelectOption(label="Moderation"),
                discord.SelectOption(label="Pic"),
                discord.SelectOption(label="Purge"),
                discord.SelectOption(label="Reactions"),
                discord.SelectOption(label="Spotify"),
                discord.SelectOption(label="Utility"),
                discord.SelectOption(label="VoiceChat")
            ]

            # Define the select menu and its callback for category selection
            class Dropdown(discord.ui.Select):
                def __init__(self):
                    super().__init__(
                        placeholder="Select a category...",
                        min_values=1,
                        max_values=1,
                        options=options,
                    )

                async def callback(self, interaction: discord.Interaction):
                    selected = self.values[0]
                    # Send a new embed with commands for the selected category
                    category_embed = discord.Embed(
                        title="Heresy Command Menu",
                        description=f"Category: {selected}",
                        color=discord.Color.blue()
                    )
                    commands_list = self.get_commands_for_category(selected)
                    command_count = len(commands_list)

                    # Format the command list for display
                    commands_display = ", ".join(commands_list)

                    # Set the commands and count in the embed description
                    category_embed.add_field(name="Commands", value=f"```{commands_display}```", inline=False)
                    category_embed.set_footer(text=f"{command_count} commands")

                    await interaction.response.send_message(embed=category_embed)

                def get_commands_for_category(self, category):
                    commands = {
                        "Alphabet": ["reply"],
                        "Application": ["aavatar", "abanner", "auserinfo"],
                        "IDLogger": ["uid", "uidban"],
                        "IDToTokenCog": ["bf"],
                        "MessageLogger": ["mnuke"],
                        "Mirror": ["mirror", "stopmirror"],
                        "Moderation": ["ban", "kick", "unban", "warn", "warnreset", "to", "uto"],
                        "Pic": ["vanity"],
                        "Purge": ["bc", "cs", "nuke", "purge", "s"],
                        "Reactions": ["ar", "arreset", "reactions", "skull", "skullreset"],
                        "Spotify": ["checkspotify", "scanspotify"],
                        "Utility": ["afk", "av", "banner", "changeav", "ping", "print"],
                        "VoiceChat": ["jvc", "leave"]
                    }
                    return commands.get(category, [])

            # Create a view to hold the dropdown
            view = discord.ui.View()
            view.add_item(Dropdown())

            # Send the embed with the dropdown menu
            await ctx.send(embed=embed, view=view)
        else:
            # Fetch detailed info for the specific command
            await self.command_help(ctx, command_name)

    async def command_help(self, ctx, command_name: str):
        # Dictionary to hold details for each command
        command_details = {
            "reply": {
                "module": "Alphabet Module",
                "description": "Replies with the most AI Generated Message ever",
                "syntax": ",reply [message]",
                "example": ",reply Hello World!",
                "permissions": "none"
            },
            "aavatar": {
                "module": "Application Module",
                "description": "Displays a user's Avatar",
                "syntax": "/aavatar [user.mention]",
                "example": "/aavatar @heresy",
                "permissions": "none"
            },
            "abanner": {
                "module": "Application Module",
                "description": "Displays a user's Banner",
                "syntax": "/abanner [user.mention]",
                "example": "/abanner @heresy",
                "permissions": "none"
            },
            "auserinfo": {
                "module": "Application Module",
                "description": "Shows the basic info of a user",
                "syntax": "/auserinfo <user.mention>",
                "example": "/auserinfo @heresy",
                "permissions": "none"
            },
            "uid": {
                "module": "IDLogger Module",
                "description": "Logs a user's UID in a .txt file",
                "syntax": ",uid <user.mention>",
                "example": ",uid @heresy",
                "permissions": "Client Side"
            },
            "uidban": {
                "module": "IDLogger Module",
                "description": "Mass bans users in `UID.txt`",
                "syntax": ",uidban",
                "example": ",uidban",
                "permissions": "Client Side"
            },
            "mnuke": {
                "module": "Message Logger",
                "description": "Nukes messages contained in a .txt file",
                "syntax": ",mnuke",
                "example": ",mnuke",
                "permissions": "Client Side"
            },
            "help": {
                "module": "Help Module",
                "description": "Shows this popup",
                "syntax": ",help [command]",
                "example": ",help",
                "permissions": "none"
            },
            "mirror": {
                "module": "Mirror Module",
                "description": "Mirror's a users messages, avatar, and display name",
                "syntax": ",mirror <user.mention>",
                "example": ",mirror @heresy",
                "permissions": "none"
            },
            "stopmirror": {
                "module": "Mirror Module",
                "description": "Stops mirroring the current user",
                "syntax": ",stopmirror",
                "example": ",stopmirror",
                "permissions": "none"
            },
            "kick": {
                "module": "Moderation Module",
                "description": "Kicks a member from the server",
                "syntax": ",kick <user> [Reason]",
                "example": ",kick @heresy Ignoring server rules",
                "permissions": "Kick Members"
            },
            "ban": {
                "module": "Moderation Module",
                "description": "Bans a member from the server",
                "syntax": ",ban <user> [reason]",
                "example": ",ban @heresy Ignoring server rules",
                "permissions": "Ban Members"
            },
            "unban": {
                "module": "Moderation Moduler",
                "description": "Unbans a user from the server",
                "syntax": ",unban <user id>",
                "example": ",unban 123456789012345678",
                "permissions": "Ban Members",
            },
            "vanity": {
                "module": "No Module",
                "description": "Changes the required vanity for pic perms",
                "syntax": ",vanity </vanity>",
                "example": ",vanity /heresy",
                "permissions": "Client Side"
            },
            "status": {
                "module": "No Module",
                "description": "Sets the bots custom status",
                "syntax": ",status <status>",
                "example": ",status Hello World!",
                "permissions": "Client Side"
            },
            "bc": {
                "module": "Purge Module",
                "description": "Purges bot commands from the last 10m",
                "syntax": ",bc",
                "example": ",bc",
                "permissions": "Manage Messages"
            },
            "cs": {
                "module": "Purge Module",
                "description": "Clears sniped messages"
            }
            # Add more commands here with their details...
        }

        # Fetch the details for the given command
        command_info = command_details.get(command_name.lower())
        
        if command_info:
            # Create an embed with the command details, no "Description" label visible
            embed = discord.Embed(
                title=f"{command_info['module']}",
                description=f"{command_info['description']}\n```ruby\nSyntax: {command_info['syntax']}\nExample: {command_info['example']}\n```",
                color=discord.Color.blue()
            )
            embed.add_field(name="Permissions", value=command_info['permissions'])
            
            # Send the embed with command details
            await ctx.send(embed=embed)
        else:
            # If the command is not found
            await ctx.send(f"No information found for the command: `{command_name}`")

# Set up the cog
async def setup(bot):
    await bot.add_cog(HelpCog(bot))
