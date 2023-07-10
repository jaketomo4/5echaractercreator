# Standard Imports
import requests
import json
import math

# Third-Party Imports
import discord
from discord import app_commands
from discord.ext import commands

# Creates a class for the d20 cog
class races(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        # Creates dictionaries for the races and subraces
        self.races = {}
        self.subraces = {}
        # Creates a joint dictionary
        self.joint = {}

    # Establishes the command related to the cog
    @app_commands.command(name="race", description="Select which race you want to play!")
    async def race(self, interaction: discord.Interaction):
        # Calls the function to get all the races and subraces
        await self.json_get()
        await interaction.response.send_message(content=f"What race would you like to play as?", view=self.SelectView(interaction, self.joint), ephemeral=True)

    # A function for getting the json from the 5etools github
    async def json_get(self):
        # Request from the 5etools github
        f = requests.get("https://raw.githubusercontent.com/5etools-mirror-1/5etools-mirror-1.github.io/master/data/races.json")
        # Uses loads for the data, not load for the file path - uses .text for the input
        json_dict = json.loads(f.text)
        # Call the tidy dictionary function
        await self.tidy_dict(json_dict)

    # A function for making nicer dictionaries
    async def tidy_dict(self, json_dict):
        # Grab the races and subraces, turning them into lists
        races = json_dict["race"]
        subraces = json_dict["subrace"]
        
        # Loops through the list of dictionaries and creates a dictionary for races
        for i in races:
            name = i.pop("name")
            self.races[name] = i

        # Loops through the list of dictionaries and creates a dictionary for subraces
        for i in subraces:
            # Try to see if the subrace is a name specific or if it is related to abilities
            try:
                # Create variables of the name and racename (to allow the try-except to work properly)
                sub_name = i.pop("name")
                race_name = i.pop("raceName")
                # Add to the dictionary with race name and subrace
                name = f"{race_name} ({sub_name})"
                self.subraces[name] = i
            except:
                # If it is a variant subrace, note such
                name = f"{i['raceName']} (Variant)"
                self.subraces[name] = i
        
        await self.join_dict()
    
    # A function for joining the dictionaries
    async def join_dict(self):
        # Assign local variables
        races = self.races
        subraces = self.subraces

        # Joins the dictionaries
        joint = races | subraces
        self.joint = sorted(joint.keys())

    # Create a Select Menu class
    class SelectRace(discord.ui.Select):
        def __init__(self, interaction: discord.Interaction, joint_dict, page):
            # Stores the passed in variables
            self.interaction = interaction
            self.joint = joint_dict
            options = [discord.SelectOption(label="default")]
            self.page = page
            super().__init__(placeholder="Races...", options=options, row=0)
            self.initiate_options()
        
        def initiate_options(self):
            # Clear the default options
            self.options.clear()
            # Make a count for the options
            count = 0
            # Make an index for the "dictionary"
            index = (self.page - 1) * 25
            # Set the end index of the "dictionary"
            end = self.page * 25
            # Calculate if the end index is greater than the total number of races/ subraces. If so, set it to the length of the "dictionary"
            if end > len(self.joint):
                end = len(self.joint)
            while index != end:
                self.options.append(discord.SelectOption(label=f"{self.joint[index]}"))
                # Add 1 to the count/ index 
                count += 1
                index += 1

        # Called when a value is selected
        async def callback(self, interaction: discord.Interaction):
            # Edit the original message
            await interaction.response.edit_message(content=f"Race selected...", view=None)
            await interaction.channel.send(content=f"{interaction.user.mention} as chosen to be a **{self.values}**")
    
    # Create a Select Menu View class to allow for discord to view it
    class SelectView(discord.ui.View):
        def __init__(self, interaction: discord.Interaction, joint_dict, page: int = 1):
            super().__init__()
            self.select = races.SelectRace(interaction, joint_dict, page)
            self.add_item(self.select)
            self.dict_len = len(joint_dict)
            # Creates a variables for the select menu class to assign the values of the dictionaries accordingly
            self.page = page
            # Creates a variable for the joint dictionary
            self.joint_dict = joint_dict
        
        @discord.ui.button(emoji="⬅️", style=discord.ButtonStyle.red, disabled=True, row=1)
        async def previous(self, interaction: discord.Interaction, Button: discord.ui.Button):
            self.page -= 1
            await self.update_view(interaction)

        @discord.ui.button(emoji="➡️", style=discord.ButtonStyle.green, disabled=False, row=1)
        async def next(self, interaction: discord.Interaction, Button: discord.ui.Button):
            self.page += 1
            await self.update_view(interaction)
                
        # Creates a function for updating the view
        async def update_view(self, interaction):
            # Checks the children
            for i in self.children:
                # Checks to see if the child is buttons (try) or SelectView (except)
                try:
                    # If the child is previous
                    if i.emoji.name == "⬅️":
                        # Check the page count and make the button function correctly
                        if self.page == 1:
                            i.style = discord.ButtonStyle.red
                            i.disabled = True
                        else:
                            i.style = discord.ButtonStyle.green
                            i.disabled = False
                    # If the child is next
                    if i.emoji.name == "➡️":
                        # Check the page count againt the length of the dictionary divided by number of max entries per select menu "page", rounded up (to allow for displaying all) and make the button function correctly
                        if self.page == (math.ceil(self.dict_len / 25)):
                            i.style = discord.ButtonStyle.red
                            i.disabled = True
                        else:
                            i.style = discord.ButtonStyle.green
                            i.disabled = False
                except:
                    self.select.page = self.page
                    self.select.initiate_options()
            await interaction.response.edit_message(view=self)

# Sets up the cog for the bot to register it
async def setup(client: commands.Bot) -> None:
    await client.add_cog(races(client))
