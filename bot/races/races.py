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
        self.joint = {}

    # Establishes the command related to the cog
    @app_commands.command(name="race", description="Select which race you want to play!")
    async def race(self, interaction: discord.Interaction):
        # Assign an ability role checker
        check = await self.check_roles(interaction)
        if check:
            await interaction.response.send_message(content=f"You already have your class selected, would you like to reset it?", view=self.ResetRace(interaction, self), ephemeral=True)
        else:
            # Calls the function to get all the races and subraces
            json_dict = await self.json_get()
            # Tidy the dictionary up
            await self.tidy_dict(json_dict)
            await interaction.response.send_message(content=f"What race would you like to play as?", view=self.SelectView(interaction, self.joint), ephemeral=True)


    # Creates a function for checking the roles
    async def check_roles(self, interaction: discord.Interaction):
        # Assigns the user's roles to a variable
        roles = interaction.user.roles
        # Loops through the user's roles
        for role in roles:
            # Gets the colour
            clr = role.colour
            # Removes hashtag
            clr = str(clr).replace("#","")
            # Loops through the string and adds the total
            total = 0
            # The likelihood is the total should be formed from either an "ability score" role or a "race" role, and a "race" role with have a total of 6 or less (Human will give the max)
            for i in clr:
                # Try to see if the digit is an int
                try:
                    total += int(i)
                except:
                    total = 0
                    break
            # If the break isn't hit, go forth
            else:
                if total <= 6 and total != 0:
                    return True
        return False
    
    # Creats a function for removing race roles
    async def remove_roles(self, interaction: discord.Interaction):
        # Assigns the user's roles to a variable
        roles = interaction.user.roles
        # Loops through the user's roles
        for role in roles:
            # Gets the colour
            clr = role.colour
            # Removes hashtag
            clr = str(clr).replace("#","")
            # Loops through the string and adds the total
            total = 0
            # The likelihood is the total should be formed from either an "ability score" role or a "race" role, and a "race" role with have a total of 6 or less (Human will give the max)
            for i in clr:
                # Try to see if the digit is an int
                try:
                    total += int(i)
                except:
                    total = 0
                    break
            # If the break isn't hit, go forth
            else:
                if total <= 6 and total != 0:
                    # Removes the roles
                    await interaction.user.remove_roles(role, atomic=True)
    
    # Creates a class for the confirmation of resetting abilities
    class ResetRace(discord.ui.View):
        def __init__(self, interaction: discord.Interaction, outer_class):
            super().__init__(timeout=None)
            self.outer_class = outer_class

        @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
        async def accept(self, interaction: discord.Interaction, Button: discord.ui.Button):
            # Calls the function to get all the races and subraces
            json_dict = await self.outer_class.json_get()
            # Tidy the dictionary up
            await self.outer_class.tidy_dict(json_dict)
            dict = self.outer_class.joint
            await interaction.response.edit_message(content=f"What race would you like to play as?", view=races.SelectView(interaction, dict))
            await races.remove_roles(races, interaction)

        @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
        async def decline(self, interaction: discord.Interaction, Button: discord.ui.Button):
            await interaction.response.edit_message(content=f"Your race has been unchanged.", view=None)

    # A function for getting the json from the 5etools github
    async def json_get(self):
        # Request from the 5etools github
        f = requests.get("https://raw.githubusercontent.com/5etools-mirror-1/5etools-mirror-1.github.io/master/data/races.json")
        # Uses loads for the data, not load for the file path - uses .text for the input
        json_dict = json.loads(f.text)
        # Call the tidy dictionary function
        return json_dict

    # A function for making nicer dictionaries
    async def tidy_dict(self, json_dict):
        # Grab the races and subraces, turning them into lists
        races = json_dict["race"]
        subraces = json_dict["subrace"]
        
        # Loops through the list of dictionaries and creates a dictionary for races
        for i in races:
            name = f"{i['name']} ({i['source']})"
            self.races[name] = i

        # Loops through the list of dictionaries and creates a dictionary for subraces
        for i in subraces:
            # Try to see if the subrace is a name specific or if it is related to abilities
            try:
                # Create variables of the name and racename (to allow the try-except to work properly)
                sub_name = i["name"]
                race_name = i["raceName"]
                # Add to the dictionary with race name and subrace
                name = f"{race_name} - {sub_name} ({i['source']})"
                self.subraces[name] = i
            except:
                # If it is a variant subrace, note such
                name = f"{i['raceName']} - Variant ({i['source']})"
                self.subraces[name] = i
        
        await self.join_dict()
    
    # A function for joining the dictionaries
    async def join_dict(self):
        # Join the dictionaries
        joint = self.races | self.subraces
        self.joint = sorted(joint.keys())

    # A function for taking the selected class and accessing the dictionary
    async def dict_access(self, interaction, option):
        # Obtain the dictionary
        json_dict = await self.json_get(self)
        # Create a variable for the entry
        entry = {}
        # Bypass the option coming through as a list
        option = option[0]
        # Assign the name from splitting on the -
        split_list = option.split(" - ")
        # Check if the option is a subrace
        if " - " in option:
            name = split_list[0]
            # Assign the raceName from split list and then splitting on the ( and removing the whitespace at the end
            raceName = (split_list[1].split("(")[0])[:-1]
            # Loop through the subraces
            for i in json_dict["subrace"]:
                # Try to see if the subrace has a name
                try:
                    # Check if i is equal to what the player entered
                    if i.get('name') == raceName:
                        # Assign the entry dictionary as the correct dictionary from the web
                        entry = i
                        break
                except(KeyError):
                    if raceName in i.values():
                        # Assign the entry dictionary as the correct dictionary from the web
                        entry = i
                        break
        else:
            name = (split_list[0].split("(")[0])[:-1]
            # Loop through the races
            for i in json_dict["race"]:
                if i.get('name') == name:
                    # Assign the entry dictionary as the correct dictionary from the web
                    entry = i
                    break
        # Throw the entry into the function for establishing important race features
        await self.race_features(self, interaction, option, entry)

    # Create the function for establishing the race features
    async def race_features(self, interaction: discord.Interaction, option, entry):
        print(entry)

        # TODO - Make this section a different function to allow for the "choose" option to occur before it and not have multiple parameters flittering about

        # Assign lists for ability increase
        skill_list = []
        score_list = []
        # Check if the entry has ability score increase
        try:
            # Create a dictionary for the racial ASI
            asi = entry.get('ability')[0]
            # Loop through the dictionary keys
            for i in asi.keys():
                # Ensure the user doesn't have to choose any abilities
                if i != 'choose':
                    # Add the skill to the list
                    skill_list.append(i)
                    # Add the score increase to the list
                    score_list.append(asi[i])
        except:
            print("no ability")

        # Do a try except to make sure abilities are there still
        try:
            # Create a dictionary for the racial ASI again
            asi = entry.get('ability')[0]
            # Check if the user can choose
            if "choose" in asi:
                # Set the dictionary for the choose options
                abi_dict = asi.get('choose')
                # Set a list for the options that can be increase
                abi_options = abi_dict['from']
                # Set a value for the amount of +1s the user can do
                abi_count = abi_dict['count']
                await interaction.response.edit_message(content=f"You have {abi_count} +1s to choose...", view=self.ChooseAbilities(interaction, abi_options, abi_count), ephemeral=True)
            else:
                # Confirm what the user selected
                await interaction.channel.send(content=f"{interaction.user.mention} has chosen to be a **{option}**")
                await self.race_role(self, interaction, option, skill_list, score_list)
        except:
            print("no ability")

    # Creates a class for the user to choose their abilities if they're able to
    class ChooseAbilities(discord.ui.View):
        def __init__(self, interaction: discord.Interaction, options, count):
            super().__init__(timeout=None)
            self.options = options
            self.count = count

        @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
        async def accept(self, interaction: discord.Interaction, Button: discord.ui.Button):
            await interaction.response.edit_message(content=f"What race would you like to play as?", view=races.SelectView(interaction, dict))
            await races.remove_roles(races, interaction)

        @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
        async def decline(self, interaction: discord.Interaction, Button: discord.ui.Button):
            await interaction.response.edit_message(content=f"Your race has been unchanged.", view=None)

    async def race_role(self, interaction: discord.Interaction, option, abilities, scores):
        # Assign the server
        server = interaction.guild
        # Create the colour string
        clrstr = "0x"
        # Creates a list of potential abilities
        abi = ["str", "dex", "con", "int", "wis", "cha"]
        
        # Loop throuhg the potential abilities to check if the race has the specific ability increase
        for i in abi:
            if i in abilities:
                index = abilities.index(i)
                clrstr += str(scores[index])
            else:
                clrstr += "0"
        # Turn the string into a colour using from_str
        colour = discord.Color.from_str(clrstr)

        # Assigns the server's roles to a variable
        roles = server.roles
        # Loops through the server's roles, if no break is hit, go into the else
        for role in roles:
            # Checks if it is an "ability score" role
            if role.name == f"{option}" and role.color == colour:
                # Assign the role to the user
                await interaction.user.add_roles(role)
                break
        else:
            # Role with matching colour hasn't been found, create role
            role = await server.create_role(name=f"{option}", color=colour)
            # Assign the role to the user
            await interaction.user.add_roles(role)

    # Create a Select Menu class
    class SelectRace(discord.ui.Select):
        def __init__(self, interaction: discord.Interaction, joint_dict, page):
            # Stores the passed in variables
            self.interaction = interaction
            self.joint = joint_dict
            options = [discord.SelectOption(label="default")]
            # Sets the page
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
            selection = self.values
            await races.dict_access(races, interaction, selection)
    
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
