# Standard Imports
import random

# Third-Party Imports
import discord
from discord import app_commands
from discord.ext import commands

# Creates a class for the d20 cog
class d20(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    # Establishes the command related to the cog
    @app_commands.command(name="d20", description="Roll a d20!")
    async def d20(self, interaction: discord.Interaction):
        # Gets a random number from 1 to 20
        roll = random.randint(1, 20)
        # Sends the message accordingly
        await interaction.response.send_message(content=
            f"You rolled a **{roll}**")

# Sets up the cog for the bot to register it
async def setup(client: commands.Bot) -> None:
    await client.add_cog(d20(client))
