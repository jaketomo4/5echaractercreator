"""
5e Character Creator
Discord Bot

Created by Jake Thompson @jaketomo4

main.py
"""

# Standard Imports
import os
import json
import time
from colorama import Fore

# Third-Party Imports
import discord
from discord.ext import commands

TIME = time.time()
print(Fore.GREEN + TIME + Fore.RESET)

# Creates a class for the client (bot) to run from
class Client(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=discord.Intents().all())
        # Define all the cogs
        self.cog_list = [
            "dice.d20",
            "ability_scores.abilities",
            "races.races"
            ]

    async def setup_hook(self):
        """Create the setup hook"""
        for ext in self.cog_list:
            await self.load_extension(ext)
    
    async def on_ready(self):
        """Print useful information when the bot is ready"""
        print(Fore.GREEN + self.user.name + Fore.RESET + " - " + Fore.YELLOW + str(self.user.id) + Fore.RESET)
        synced = await self.tree.sync()
        print(Fore.RED + "Synced " + Fore.MAGENTA + str(len(synced)) + " commands" + Fore.RESET)
        print(Fore.RED + "Time taken: " + Fore.GREEN + (time.time() - TIME) + Fore.RED + " seconds" + Fore.RESET)

# Assigns the class
client = Client()

# Reads the config file to get the token
with open("config.json", "r") as f:
    data = json.load(f)
    TOKEN = data["TOKEN"]

# Runs the client
client.run(TOKEN)
