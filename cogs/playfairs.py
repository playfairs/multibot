import discord
from discord.ext import commands
from discord import app_commands

class exodusCog(commands.Cog):  # Changed class name to reflect the new bot name
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='about', description="Displays information about Playfair or Heresy.")
    @app_commands.describe(option="Select either Playfair or Heresy")
    @app_commands.choices(
        option=[
            app_commands.Choice(name="Playfair", value="playfair"),  # Use lowercase value for comparison
            app_commands.Choice(name="Heresy", value="heresy"),  # Updated value for the new bot name
        ]
    )
    async def about(self, interaction: discord.Interaction, option: app_commands.Choice[str]):
        """Displays information about Playfair or Heresy in an embed."""
        option_value = option.value.lower()  # Lowercase the value for uniform comparison
        
        # Check the value directly, since it's already set to lowercase
        if option_value == 'playfair':
            embed = discord.Embed(
                title="About Playfair",
                description="Developer of Heresy and other Discord Bots.",
                color=discord.Color.pink()
            )
            embed.add_field(name="Developer", value="<@785042666475225109>", inline=False)
            embed.add_field(name="Description", value="Playfairs, or Playfair, is the Bot Developer of this and many other bots, also being the owner of /heresy, that is all <33", inline=False)
            embed.add_field(name="Useful Links", value="[guns.lol](https://guns.lol/playfair) | [about.me](https://about.me/creepfully)", inline=False)
            embed.set_footer(text="For more information, visit https://about.me/creepfully to learn more about the Bot Developer.")
        
        elif option_value == 'heresy':  # Changed the condition to reflect the new bot name
            embed = discord.Embed(
                title="About Heresy",  # Updated embed title
                description="Discord Bot created and coded by <@785042666475225109>.",
                color=discord.Color.green()
            )
            embed.add_field(name="Developer", value="<@785042666475225109>", inline=False)
            embed.add_field(name="Description", value="Heresy is a multifunctional Discord Bot created by <@785042666475225109>, serving many purposes.", inline=False)  # Updated description
            embed.set_footer(text="For more information, DM @playfairs, or check /help for more info.")
        
        await interaction.response.send_message(embed=embed)

    @app_commands.command(name='links', description="Displays useful links.")
    async def links(self, interaction: discord.Interaction):
        """Displays useful links."""
        links_info = (
            "**Useful Links:**\n"
            "- [guns.lol](https://guns.lol/playfair)\n"
            "- [wanted.lol](https://wanted.lol/suicideboys)\n"
            "- [about.me](https://about.me/creepfully)\n"
            "- [TikTok](https://tiktok.com/creepfully)\n"
            # Add more links as needed
        )
        await interaction.response.send_message(links_info)

# Async setup function to add the cog to the bot
async def setup(bot):
    await bot.add_cog(exodusCog(bot))  # Updated cog name
