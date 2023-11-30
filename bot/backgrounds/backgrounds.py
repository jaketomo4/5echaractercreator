"""
5e Character Creator
Discord Bot

Created by Jake Thompson @jaketomo4

backgrounds.py
"""

# Standard Imports
import requests
import json
import math

#Third-Party Imports
import discord
from discord import app_commands
from discord.ext import commands

# Create the URL variable for the github link to 5etools
URL = "https://raw.githubusercontent.com/5etools-mirror-1/5etools-mirror-1.github.io/master/data/backgrounds.json"

# Creates a class for the backgrounds cog
class backgrounds(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        # Creates a dictionary for the backgrounds
        self.dict = {}

    # Establishes the command related to the cog
    @app_commands.command(name="background", description="Select your background!")
    async def background(self, interaction: discord.Interaction):
        """Slash command for background"""
        # Assign a role checker variable
        check = await self.check_roles(interaction)
        if check:
            await interaction.response.send_message(content=f"You already have your background selected, would you like to reset it?", view=self.ResetBackground(interaction, self), ephemeral=True)
        else:
            # Calls the function to get all the backgrounds
            json_dict = await self.json_get()
            # Tidy the dictionary
            await self.tidy_dict(json_dict)
            await interaction.response.send_message(content=f"What background would you like to have?", view=self.SelectView(interaction, self.dict), ephemeral=True)

    # Creates a function for checking the roles
    async def check_roles(self, interaction: discord.Interaction):
        """Check the user's roles"""
        # Assigns the user's roles to a variable
        roles = interaction.user.roles
        # Loops through the user's roles
        for role in roles:
            # TODO: Establish the method the background role is stored and amend accordingly
            # Check the role name
            if role.name == "background":
                return True
        return False
    
    # Creates a function for removing background roles
    async def remove_roles(self, interaction: discord.Interaction):
        """Remove the user's roles"""
        # Assigns the user's roles to a variable
        roles = interaction.user.roles
        # Loops through the user's roles
        for role in roles:
            # TODO: Establish the method the background role is stored and amend accodingly
            # Check the role name
            if role.name == "background":
                await interaction.user.remove_roles(role, atomic=True)

    # Creates a class for the confirmation of resetting the background
    class ResetBackground(discord.ui.View):
        def __init__ (self, interaction: discord.Interaction, outer_class):
            super().__init__(timeout=None)
            self.outer_class = outer_class

        @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
        async def accept(self, interaction: discord.Interaction, Button: discord.ui.Button):
            """Accept a background change"""
            # Calls the function to get all the backgrounds
            json_dict = await self.outer_class.json_get()
            # Tidy the dictionary
            await self.outer_class.tidy_dict(json_dict)
            dict = self.outer_class.dict
            await interaction.response.edit_message(content=f"What background would you like to have?", view=backgrounds.SelectView(interaction, dict))
            await backgrounds.remove_roles(backgrounds, interaction)

        @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
        async def decline(self, interaction: discord.Interaction, Button: discord.ui.Button):
            """Decline a background change"""
            await interaction.response.edit_message(content=f"Your background has been unchanged.", view=None)

    # A function for getting the json from the 5etools github
    async def json_get(self):
        """Get the json for backgrounds"""
        # Request from the 5etools github
        f = requests.get(URL)
        # Uses loads for the data, not load for the file path - uses .text for the input
        json_dict = json.loads(f.text)
        # Call the tidy dictionary function
        return json_dict
    
    # A function for making nicer dictionaries
    async def tidy_dict(self, json_dict):
        """Tidy the json"""
        # Grab the backgrounds, turning them into lists
        backgrounds = json_dict["background"]

        # Loops through the list of dictionaries and creates a dictionary for backgrounds
        for i in backgrounds:
            name = f"{i['name']} ({i['source']})"
            self.dict[name] = i

    # A function for taking the selected background and accessing the dictionary
    async def dict_access(self, interaction, option):
        """Access the dictionary"""
        # Obtain the dictionary
        json_dict = await self.json_get(self)
        # Create a variable for the entry
        entry = {}
        # Bypass the option coming through as a list
        option = option[0]
        name = option.split("(")[0][:-1]
        # Loop through the backgrounds
        for i in json_dict["background"]:
            if i.get('name') == name:
                # Assign the entry dictionary as the correct dictionary from the web
                entry = i
                break
        # Throw the entry into the function for establishing important background features
        await self.choose_check(self, interaction, option, entry)

    #Create the fucntion for establishing the background features
    async def choose_check(self, interaction: discord.Interaction, option, entry):
        """Check if the race has any important choosable features"""
        # TODO: Skill Proficiencies, Language Proficiences, Characteristics (traits)

    # Creates a Select Menu class
    class SelectBackground(discord.ui.Select):
        def __init__(self, interaction: discord.Interaction, dict, page):
            # Stores the pass in variables
            self.interaction = interaction
            self.dict = dict
            options = [discord.SelectOption(label="default")]
            # Sets the page
            self.page = page
            super().__init__(placeholder="Backgrounds...", options=options, row=0)
            self.initiate_options()

        def initiate_options(self):
            """Fill the Select Menu"""
            # Clear the default options
            self.options.clear()
            # Make a count for the options
            count = 0
            # Make an index for the dictionary
            index = (self.page - 1) * 25
            # Set the end index of the dictionary
            end = self.page * 25
            # Calculate if the end index is greater than the total number of backgrounds
            if end > len(self.dict):
                end = len(self.dict)
            while index != end:
                self.options.append(discord.SelectOption(label=f"{self.dict[index]}"))
                # Add 1 to the count/ index
                count += 1
                index += 1

        # Called when a value is selected
        async def callback(self, interaction: discord.Interaction):
            """Assess the select choice"""
            # Edit the original message
            await interaction.response.edit_message(content=f"Background select...", view=None)
            selection = self.values
            await backgrounds.dict_access(backgrounds, interaction, selection)
    
    # Create a Select Menu View class to allow for discord to view it
    class SelectView(discord.ui.View):
        def __init__(self, interaction: discord.Interaction, dict, page: int = 1):
            super().__init__()
            self.select = backgrounds.SelectBackground(interaction, dict, page)
            self.add_item(self.select)
            self.dict_len = len(dict)
            # Creates a variable for the select menu class to assign the page
            self.page = page
            # Creates a variable for the dictionary
            self.dict = dict

        @discord.ui.button(emoji="⬅️", style=discord.ButtonStyle.red, disabled=True, row=1)
        async def previous(self, interaction: discord.Interaction, Button: discord.ui.Button):
            """Go to the previous page on the select menu"""
            self.page -= 1
            await self.update_view(interaction)

        @discord.ui.button(emoji="➡️", style=discord.ButtonStyle.green, disabled=False, row=1)
        async def next(self, interaction: discord.Interaction, Button: discord.ui.Button):
            """Go to the next page on the select menu"""
            self.page += 1
            await self.update_view(interaction)

        # Creates a function for updating the view
        async def update_view(self, interaction: discord.Interaction):
            """Updates the view of the select menu"""
            # Checks the children
            for i in self.children:
                # Chekcs to see if the child is a button (try) or SelectView (except)
                try:
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
    """Setup the cog"""
    await client.add_cog(backgrounds(client))

