"""
5e Character Creator
Discord Bot

Created by Jake Thompson @jaketomo4

skills.py
"""

# Standard Imports
import requests
import json

# Third-Party Imports
import discord
from discord import app_commands
from discord.ext import commands

# Create the URL variable for the github link to 5etools
URL = "https://raw.githubusercontent.com/5etools-mirror-1/5etools-mirror-1.github.io/master/data/skills.json"

# Creates a class for the skills cog
class skills(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    # Establishes the command related to the cog
    @app_commands.command(name="skills", description="Make a skill check!")
    async def skills(self, interaction: discord.Interaction):
        """Slash command for skills"""
        # TODO: Perform a check to see if the user has all class creation complete before being able to use this command. Maybe send back what they haven't set up?
        pass

# Sets up the cog for the bot to register it
async def setup(client: commands.Bot) -> None:
    """Setup the cog"""
    await client.add_cog(skills(client))