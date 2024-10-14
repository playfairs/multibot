import discord
from discord.ext import commands
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

class Spotify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        # Set up Spotify client
        client_id = 'bd864e6b1cdd496bacff9a8cdf302262'
        client_secret = 'ab91c46e4b959743aba2cde6e49d04e2ed'
        credentials = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        self.sp = spotipy.Spotify(client_credentials_manager=credentials)

        # Load allowed users from file
        self.allowed_users = self.load_allowed_users()
        
        # Target channel ID to send embeds
        self.target_channel_id = 123456789012345678  # Replace with your actual channel ID

    def load_allowed_users(self):
        """Loads the allowed users from a text file."""
        if os.path.exists("allowed_users.txt"):
            with open("allowed_users.txt", "r") as f:
                return set(line.strip() for line in f)
        return set()

    def save_allowed_user(self, user_id):
        """Saves a new allowed user to the text file."""
        with open("allowed_users.txt", "a") as f:
            f.write(f"{user_id}\n")

    @commands.hybrid_command(name="scanspotify", with_app_command=True)
    async def scanspotify(self, ctx):
        """Allows the bot to scan the user's Spotify activity."""
        print("scanspotify command triggered.")  # Debug statement
        user_id = str(ctx.author.id)

        if user_id in self.allowed_users:
            await ctx.send("You are already registered for Spotify scanning.")
        else:
            self.allowed_users.add(user_id)
            self.save_allowed_user(user_id)
            await ctx.send("You have been registered for Spotify scanning.")

    @commands.hybrid_command(name="checkspotify", with_app_command=True)
    async def checkspotify(self, ctx):
        """Scans all users in the guild for Spotify activity."""
        print("checkspotify command triggered.")  # Debug statement
        found_user = False

        # Log all member activities and check for Spotify
        for member in ctx.guild.members:
            if member.activity and isinstance(member.activity, discord.Spotify):
                found_user = True
                activity = member.activity

                # Get the current track details
                track_name = activity.title
                artist_name = activity.artist
                track_duration = activity.duration.total_seconds()
                track_duration_minutes = int(track_duration // 60)
                track_duration_seconds = int(track_duration % 60)
                track_url = activity.url

                # Fetch additional details from Spotify API
                try:
                    track_info = self.sp.track(activity.track_id)
                    cover_image_url = track_info['album']['images'][0]['url'] if track_info['album']['images'] else None
                    
                    # Create the embed
                    embed = discord.Embed(
                        title=track_name,
                        description=f"**Artist:** {artist_name}\n**Duration:** {track_duration_minutes}m {track_duration_seconds}s\n**Link:** [Listen Here]({track_url})",
                        color=0xB22222  # Dark red color
                    )
                    if cover_image_url:
                        embed.set_thumbnail(url=cover_image_url)

                    # Send the embed to the specified channel
                    channel = self.bot.get_channel(self.target_channel_id)
                    if channel:
                        await channel.send(embed=embed)
                        print(f"Embed sent for {member.name}.")  # Debug statement
                    else:
                        await ctx.send("Target channel not found. Please check the channel ID.")
                except Exception as e:
                    print(f"Error fetching track info for {member.name}: {str(e)}")
                    await ctx.send(f"Error fetching track info for {member.name}.")
        
        if not found_user:
            await ctx.send("No users are currently listening to Spotify.")

async def setup(bot):
    await bot.add_cog(Spotify(bot))
