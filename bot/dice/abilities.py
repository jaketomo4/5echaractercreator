# Standard Imports
import random

# Third-Party Imports
import discord
from discord import app_commands
from discord.ext import commands

# Creates a class for the abilities cog
class abilities(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        # Assigns the stats for all functions to use
        self.stats = ["Str", "Dex", "Con", "Int", "Wis", "Cha"]

    # Creates the commands for establishing ability scores
    @app_commands.command(name="abilities", description="Establish your ability scores!")
    async def abilities(self, interaction: discord.Interaction):
        # Adds a view for the user to see what they can do
        await interaction.response.send_message(content=f"Select what you'd like to do:", view=self.AbilityScores(interaction), ephemeral=True)
        # Calls the check roles function
        await self.check_roles(interaction)

    # Creates a function for checking the roles and removing them accordingly if the user uses this 
    async def check_roles(self, interaction: discord.Interaction):
        # Assigns the user's roles to a variable
        roles = interaction.user.roles
        # Loops through the user's roles
        for role in roles:
            # Checks if they are the "ability score" colour
            if role.color == discord.colour.Colour(0x0000FF):
                await interaction.user.remove_roles(role, atomic=True)

    # Creates a class for the various ability buttons
    class AbilityScores(discord.ui.View):
        def __init__(self, interaction: discord.Interaction):
            super().__init__(timeout=None)

        # Creates a "Standard Array" button which is green and enabled
        @discord.ui.button(label="Standard Array", style=discord.ButtonStyle.green, disabled = False)
        async def standard_array(self, interaction: discord.Interaction, Button: discord.ui.Button):
            # Edits the original message accordingly
            await interaction.response.edit_message(content="Please select which ability you want to assign and the number you want to assign it to.", view=abilities.AbilityButtons(interaction, Button.label))

        # Creates a "Rolling Stats" button which is green and enabled
        @discord.ui.button(label="Rolling Stats", style=discord.ButtonStyle.green, disabled = False)
        async def rolling_stats(self, interaction: discord.Interaction, Button: discord.ui.Button):
            # Defines the class to bypass async being used in __init__
            roll_stats = abilities.RollingStats(interaction, Button, Button.label)
            # Calls roll stats
            await roll_stats.roll_stats(interaction)

        # Creates a "Point Buy" button which is green and enabled
        @discord.ui.button(label="Point Buy", style=discord.ButtonStyle.green, disabled = False)
        async def point_buy(self, interaction: discord.Interaction, Button: discord.ui.Button):
            # Edits the original message accordingly
            await interaction.response.edit_message(content="Please select which ability you want to increment/ decrement", view=abilities.PointBuy(interaction, Button.label))
    
    # Creates a class for Rolling Stats
    class RollingStats(discord.ui.View):
        def __init__(self, interaction: discord.Interaction, Button: discord.ui.Button, ability_type):
            super().__init__(timeout=None)
            self.ability_type = ability_type
            # Creates a variable for the array to pass into the choosing buttons
            self.totals = []
        
        # Creates a button for the stats to be rerolled
        @discord.ui.button(label="Re-roll?", style=discord.ButtonStyle.red, disabled=False)
        async def reroll(self, interaction: discord.Interaction, Button:discord.ui.Button):
            # Rerolls the stats
            await self.roll_stats(interaction)

        # Creates a button for the stats to be rerolled
        @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green, disabled=False)
        async def confirm(self, interaction: discord.Interaction, Button:discord.ui.Button):
            # Confirms the rolled stats
            await interaction.response.edit_message(content="Please select which ability you want to assign and the number you want to assign it to.", view=abilities.AbilityButtons(interaction, Button.label, self.totals))

        async def roll_stats(self, interaction: discord.Interaction):
            response = f"You rolled:\n"
            # Creates a nested rolls list for all rolls
            nest_rolls = []
            # Creates a totals list
            totals = []
            # Assigns counter variable
            j = 0
            while j < 6:
                # Assigns a counter variable
                i = 0
                # Assigns the total variable
                total = 0
                # Creates a rolls list for each iteration
                rolls = []
                while i < 4:
                    # Rolls a d6
                    roll = random.randint(1, 6)
                    # Adds to the rolls list
                    rolls.append(roll)
                    # Adds to the total
                    total += roll
                    # Pluses the counter
                    i += 1
                # Drops the lowest
                total -= min(rolls)
                # Adds the total to the list
                totals.append(total)
                # Adds to the nested rolls
                nest_rolls.append(rolls)
                j += 1
            
            index = 0
            for i in nest_rolls:
                response = (f"{response}{i} = **{totals[index]}**\n")
                index += 1
            
            self.totals = totals

            await interaction.response.edit_message(content=f"{response}\nDo you wish to reroll?", view=self)

    # Creates a class for Point Buy
    class PointBuy(discord.ui.View):
        def __init__(self, interaction: discord.Interaction, ability_type):
            super().__init__(timeout=None)
            self.ability_type = ability_type
            self.abilities = ["Str", "Dex", "Con", "Int", "Wis", "Cha"]
            self.points = 27

        # Creates buttons for the various stats
        @discord.ui.button(label="Str | 8", style=discord.ButtonStyle.blurple, disabled=False, row=1)
        async def str(self, interaction: discord.Interaction, Button: discord.ui.Button):
            # Checks the button style, if it's one colour, change it to the other
            if Button.style == discord.ButtonStyle.blurple:
                Button.style = discord.ButtonStyle.green
            else:
                Button.style = discord.ButtonStyle.blurple
            await self.update_button(interaction, Button)
        @discord.ui.button(label="Dex | 8", style=discord.ButtonStyle.blurple, disabled=False, row=2)
        async def dex(self, interaction: discord.Interaction, Button: discord.ui.Button):
            # Checks the button style, if it's one colour, change it to the other
            if Button.style == discord.ButtonStyle.blurple:
                Button.style = discord.ButtonStyle.green
            else:
                Button.style = discord.ButtonStyle.blurple
            await self.update_button(interaction, Button)
        @discord.ui.button(label="Con | 8", style=discord.ButtonStyle.blurple, disabled=False, row=3)
        async def con(self, interaction: discord.Interaction, Button: discord.ui.Button):
            # Checks the button style, if it's one colour, change it to the other
            if Button.style == discord.ButtonStyle.blurple:
                Button.style = discord.ButtonStyle.green
            else:
                Button.style = discord.ButtonStyle.blurple
            await self.update_button(interaction, Button)
        @discord.ui.button(label="Int | 8", style=discord.ButtonStyle.blurple, disabled=False, row=1)
        async def int(self, interaction: discord.Interaction, Button: discord.ui.Button):
            # Checks the button style, if it's one colour, change it to the other
            if Button.style == discord.ButtonStyle.blurple:
                Button.style = discord.ButtonStyle.green
            else:
                Button.style = discord.ButtonStyle.blurple
            await self.update_button(interaction, Button)
        @discord.ui.button(label="Wis | 8", style=discord.ButtonStyle.blurple, disabled=False, row=2)
        async def wis(self, interaction: discord.Interaction, Button: discord.ui.Button):
            # Checks the button style, if it's one colour, change it to the other
            if Button.style == discord.ButtonStyle.blurple:
                Button.style = discord.ButtonStyle.green
            else:
                Button.style = discord.ButtonStyle.blurple
            await self.update_button(interaction, Button)
        @discord.ui.button(label="Cha | 8", style=discord.ButtonStyle.blurple, disabled=False, row=3)
        async def cha(self, interaction: discord.Interaction, Button: discord.ui.Button):
            # Checks the button style, if it's one colour, change it to the other
            if Button.style == discord.ButtonStyle.blurple:
                Button.style = discord.ButtonStyle.green
            else:
                Button.style = discord.ButtonStyle.blurple
            await self.update_button(interaction, Button)

        # Creates button for the total point
        @discord.ui.button(label="27", style=discord.ButtonStyle.grey, disabled=True, row=1)
        async def total(self, interaction: discord.Interaction, Button: discord.ui.Button):
            print("total")

        # Creates buttons for incrementing or decrementing
        @discord.ui.button(label="+", style=discord.ButtonStyle.green, disabled=False, row=2)
        async def plus(self, interaction: discord.Interaction, Button: discord.ui.Button):
            # Loop through the children to see which ability is selected
            for i in self.children:
                # Check it's green (selected)
                if i.style == discord.ButtonStyle.green and i.label != "+":
                    # Split the label
                    label = i.label.split(" | ")
                    # Assign the number and add one
                    num = int(label[1]) + 1
                    # Performs check to see if it's 15
                    if num == 15:
                        self.points -= 2
                    else:
                        self.points -= 1
                    # Reassign the label
                    i.label = f"{label[0]} | {num}"
                    # Update the button
                    await self.update_view(interaction, Button)
                    return
        @discord.ui.button(label="-", style=discord.ButtonStyle.red, disabled=False, row=3)
        async def subtract(self, interaction: discord.Interaction, Button: discord.ui.Button):
            # Loop through the children to see which ability is selected
            for i in self.children:
                # Check it's green (selected)
                if i.style == discord.ButtonStyle.green and i.label != "+":
                    # Split the label
                    label = i.label.split(" | ")
                    # Assign the number and subtract one
                    num = int(label[1]) - 1
                    # Performs check to see if it's 15
                    if num + 1 == 15:
                        self.points += 2
                    else:
                        self.points += 1
                    # Reassign the label
                    i.label = f"{label[0]} | {num}"
                    # Update the button
                    await self.update_view(interaction, Button)
                    return
        
        # Creates button for reseting
        @discord.ui.button(label="Reset", style=discord.ButtonStyle.red, disabled=False, row=4)
        async def reset(self, interaction: discord.Interaction, Button: discord.ui.Button):
            # Loops through the buttons
            for i in self.children:
                try:
                    ability_label = Button.label.split(" | ")[0]
                except:
                    ability_label = i.label

                ###
                # TO DO - RESET button does not reset the ability buttons. Why?

                # Check if the button is an ability or a score
                if ability_label in self.abilities:
                    i.style = discord.ButtonStyle.blurple
                    # Reassign the label
                    i.label = f"{ability_label[0]} | 8"
                    # Update the button
                if i.label == str(self.points):
                    i.label = "27"
            # Reset points
            self.points = 27
            await interaction.response.edit_message(view=self)

        # A function for updating the buttons
        async def update_button(self, interaction: discord.Interaction, Button: discord.ui.Button):
            ability_label = Button.label.split(" | ")[0]
            # Check if the button is an ability or a score
            if ability_label in self.abilities:
                # Loop through the children of the view
                for i in self.children:
                    try:
                        label = i.label.split(" | ")[0]
                    except:
                        label = i.label
                    # Check if it's an ability
                    if label in self.abilities:
                        # If it's not the clicked button, turn it green
                        if i != Button:
                            i.style = discord.ButtonStyle.blurple
            await self.update_view(interaction, Button)

        # A function for updating the view
        async def update_view(self, interaction: discord.Interaction, Button: discord.ui.Button):
            # Updates the total
            self.children[6].label = f"{self.points}"
            # Checks if all the points have been used
            if self.points == 0:
                await interaction.response.edit_message(content=f"Your ability scores have been established...", view=None)
                await abilities.dict_to_msg(abilities, interaction, self.default_scores, self.ability_type)
            else:
                # Edit the message with the updated view
                await interaction.response.edit_message(view=self)

    # Creates a class for the Standard Array view
    class AbilityButtons(discord.ui.View):
        def __init__(self, interaction: discord.Interaction, ability_type, number_array = ["15", "14", "13", "12", "10", "8"]):
            super().__init__(timeout=None)
            self.ability_type = ability_type
            self.abilities = ["Str", "Dex", "Con", "Int", "Wis", "Cha"]
            self.number_array = number_array
            # Establish colour checks
            self.score = False
            self.number = False
            self.tracker = 0
            # Establish variables for tracking
            self.stat = ""
            self.num = ""
            # Creates a dictionary for the values
            self.default_scores = {
                "Strength": 10,
                "Dexterity": 10,
                "Constitution": 10,
                "Intelligence": 10,
                "Wisdom": 10,
                "Charisma": 10
            }
            # Sets a count for the number buttons
            num_count = 0
            # Loops through the children (buttons)
            for i in self.children:
                try:
                    # Checks the label is an integer
                    int(i.label)
                    i.label = self.number_array[num_count]
                    num_count += 1
                except:
                    pass

        # Creates buttons for the various stats
        @discord.ui.button(label="Str", style=discord.ButtonStyle.blurple, disabled = False, row=1)
        async def str(self, interaction: discord.Interaction, Button: discord.ui.Button):
            # Checks the button style, if it's one colour, change it to the other
            if Button.style == discord.ButtonStyle.blurple:
                Button.style = discord.ButtonStyle.green
                self.score = True
                self.stat = Button.label
            else:
                Button.style = discord.ButtonStyle.blurple
                self.score = False
            await self.update_button(interaction, Button)
        @discord.ui.button(label="Dex", style=discord.ButtonStyle.blurple, disabled = False, row=2)
        async def dex(self, interaction: discord.Interaction, Button: discord.ui.Button):
            # Checks the button style, if it's one colour, change it to the other
            if Button.style == discord.ButtonStyle.blurple:
                Button.style = discord.ButtonStyle.green
                self.score = True
                self.stat = Button.label
            else:
                Button.style = discord.ButtonStyle.blurple
                self.score = False
            await self.update_button(interaction, Button)
        @discord.ui.button(label="Con", style=discord.ButtonStyle.blurple, disabled = False, row=3)
        async def con(self, interaction: discord.Interaction, Button: discord.ui.Button):
            # Checks the button style, if it's one colour, change it to the other
            if Button.style == discord.ButtonStyle.blurple:
                Button.style = discord.ButtonStyle.green
                self.score = True
                self.stat = Button.label
            else:
                Button.style = discord.ButtonStyle.blurple
                self.score = False
            await self.update_button(interaction, Button)
        @discord.ui.button(label="Int", style=discord.ButtonStyle.blurple, disabled = False, row=1)
        async def int(self, interaction: discord.Interaction, Button: discord.ui.Button):
            # Checks the button style, if it's one colour, change it to the other
            if Button.style == discord.ButtonStyle.blurple:
                Button.style = discord.ButtonStyle.green
                self.score = True
                self.stat = Button.label
            else:
                Button.style = discord.ButtonStyle.blurple
                self.score = False
            await self.update_button(interaction, Button)
        @discord.ui.button(label="Wis", style=discord.ButtonStyle.blurple, disabled = False, row=2)
        async def wis(self, interaction: discord.Interaction, Button: discord.ui.Button):
            # Checks the button style, if it's one colour, change it to the other
            if Button.style == discord.ButtonStyle.blurple:
                Button.style = discord.ButtonStyle.green
                self.score = True
                self.stat = Button.label
            else:
                Button.style = discord.ButtonStyle.blurple
                self.score = False
            await self.update_button(interaction, Button)
        @discord.ui.button(label="Cha", style=discord.ButtonStyle.blurple, disabled = False, row=3)
        async def cha(self, interaction: discord.Interaction, Button: discord.ui.Button):
            # Checks the button style, if it's one colour, change it to the other
            if Button.style == discord.ButtonStyle.blurple:
                Button.style = discord.ButtonStyle.green
                self.score = True
                self.stat = Button.label
            else:
                Button.style = discord.ButtonStyle.blurple
                self.score = False
            await self.update_button(interaction, Button)

        # Creates buttons for the standard array values
        @discord.ui.button(label="10", style=discord.ButtonStyle.blurple, disabled = False, row=1)
        async def first(self, interaction: discord.Interaction, Button: discord.ui.Button):
            # Checks the button style, if it's one colour, change it to the other
            if Button.style == discord.ButtonStyle.blurple:
                Button.style = discord.ButtonStyle.green
                self.number = True
                self.num = Button.label
            else:
                Button.style = discord.ButtonStyle.blurple
                self.number = False
            await self.update_button(interaction, Button)
        @discord.ui.button(label="10", style=discord.ButtonStyle.blurple, disabled = False, row=2)
        async def second(self, interaction: discord.Interaction, Button: discord.ui.Button):
            # Checks the button style, if it's one colour, change it to the other
            if Button.style == discord.ButtonStyle.blurple:
                Button.style = discord.ButtonStyle.green
                self.number = True
                self.num = Button.label
            else:
                Button.style = discord.ButtonStyle.blurple
                self.number = False
            await self.update_button(interaction, Button)
        @discord.ui.button(label="10", style=discord.ButtonStyle.blurple, disabled = False, row=3)
        async def third(self, interaction: discord.Interaction, Button: discord.ui.Button):
            # Checks the button style, if it's one colour, change it to the other
            if Button.style == discord.ButtonStyle.blurple:
                Button.style = discord.ButtonStyle.green
                self.number = True
                self.num = Button.label
            else:
                Button.style = discord.ButtonStyle.blurple
                self.number = False
            await self.update_button(interaction, Button)
        @discord.ui.button(label="10", style=discord.ButtonStyle.blurple, disabled = False, row=1)
        async def fourth(self, interaction: discord.Interaction, Button: discord.ui.Button):
            # Checks the button style, if it's one colour, change it to the other
            if Button.style == discord.ButtonStyle.blurple:
                Button.style = discord.ButtonStyle.green
                self.number = True
                self.num = Button.label
            else:
                Button.style = discord.ButtonStyle.blurple
                self.number = False
            await self.update_button(interaction, Button)
        @discord.ui.button(label="10", style=discord.ButtonStyle.blurple, disabled = False, row=2)
        async def fifth(self, interaction: discord.Interaction, Button: discord.ui.Button):
            # Checks the button style, if it's one colour, change it to the other
            if Button.style == discord.ButtonStyle.blurple:
                Button.style = discord.ButtonStyle.green
                self.number = True
                self.num = Button.label
            else:
                Button.style = discord.ButtonStyle.blurple
                self.number = False
            await self.update_button(interaction, Button)
        @discord.ui.button(label="10", style=discord.ButtonStyle.blurple, disabled = False, row=3)
        async def sixth(self, interaction: discord.Interaction, Button: discord.ui.Button):
            # Checks the button style, if it's one colour, change it to the other
            if Button.style == discord.ButtonStyle.blurple:
                Button.style = discord.ButtonStyle.green
                self.number = True
                self.num = Button.label
            else:
                Button.style = discord.ButtonStyle.blurple
                self.number = False
            await self.update_button(interaction, Button)
        
        # Creates a reset button
        @discord.ui.button(label="Reset", style=discord.ButtonStyle.red, disabled=False, row=3)
        async def reset(self, interaction: discord.Interaction, Button:discord.ui.Button):
            # Re-assigns the tracker variables accordingly
            self.score = False
            self.number = False
            self.tracker = 0
            self.stat = ""
            self.num = ""
            # Loops through the children and sets them to default
            for i in self.children:
                i.disabled = False
                i.style = discord.ButtonStyle.blurple
            await self.update_button(interaction, Button)

        # A function for updating the buttons and the view
        async def update_button(self, interaction: discord.Interaction, Button: discord.ui.Button):
            # Check if the button is an ability or a score
            if Button.label in self.abilities:
                # Loop through the children of the view
                for i in self.children:
                    # Check if it's disabled, if so, skip
                    if i.disabled == False:
                        # Check if it's an ability
                        if i.label in self.abilities:
                            # If it's not the clicked button, turn it green
                            if i != Button:
                                i.style = discord.ButtonStyle.blurple
            else:
                # Loop through the children of the view
                for i in self.children:
                    # Check if it's disabled, if so, skip
                    if i.disabled == False:
                        # Checks to see it's not the reset button
                        if i.label != "Reset":
                            # Check if it's not an ability
                            if not i.label in self.abilities:
                                # If it's not the clicked button, turn it green
                                if i != Button:
                                    i.style = discord.ButtonStyle.blurple
            # Checks to see if an ability and score are selected
            if self.score and self.number:
                # Checks which stat is being assigned
                match (self.stat):
                    case "Str":
                        self.default_scores["Strength"] = int(self.num)
                    case "Dex":
                        self.default_scores["Dexterity"] = int(self.num)
                    case "Con":
                        self.default_scores["Constitution"] = int(self.num)
                    case "Int":
                        self.default_scores["Intelligence"] = int(self.num)
                    case "Wis":
                        self.default_scores["Wisdom"] = int(self.num)
                    case "Cha":
                        self.default_scores["Charisma"] = int(self.num)
                # Loop through the children to see which button is the selected and disable them
                for i in self.children:
                    if i.label == self.stat:
                        i.disabled = True
                        i.style = discord.ButtonStyle.gray
                    if i.label == self.num:
                        i.disabled = True
                        i.style = discord.ButtonStyle.gray
                self.score = False
                self.number = False
                self.tracker += 1
            
            # Checks if all the abilities have been selected
            if self.tracker == 6:
                await interaction.response.edit_message(content=f"Your ability scores have been established...", view=None)
                await abilities.dict_to_msg(abilities, interaction, self.default_scores, self.ability_type)
            else:
                # Edit the message with the updated view
                await interaction.response.edit_message(view=self)
    
    # A function for changing the dictionary to a message
    async def dict_to_msg(self, interaction, dict, type):
        # Creates lists for the abilities and numbers
        abi_list = []
        num_list = []
        # Creates the initial message
        message = f"**{type}** was used for {interaction.user.mention}'s abilities:\n"
        # Assign a string value of the dictionary
        dict_str = str(dict)
        # Replace the necessary characters - re.sub did not work as well
        dict_str = dict_str.replace("{", "").replace("}", "").replace("'", "")
        # Split the string via commas
        split_dict = dict_str.split(",")
        # Loop through the split dictionary string and add to the message accordingly
        for i in split_dict:
            # Replace the whitespaces
            no_ws = i.replace(" ", "")
            # Split using the : to allow for better discord formatting
            abi = no_ws.split(":")[0]
            abi_list.append(abi)
            num = no_ws.split(":")[1]
            num_list.append(num)
            message = f"{message}**{abi}** : **{num}**\n"
        # Send the message
        await interaction.channel.send(f"{message}")
        # Call the assign roles function
        await self.assign_roles(self, interaction, abi_list, num_list)
    
    async def assign_roles(self, interaction: discord.Interaction, ability, number):
        # A counter for the role assignment
        count = 0
        # Assign the server
        server = interaction.guild
        # Loop through the lists
        for abi in ability:
            num = number[count]
            # See if the role exists, if not, create one
            role = discord.utils.get(server.roles, name=f"{abi} {num}")
            if role == None:
                role = await server.create_role(name=f"{abi} {num}", color=0x0000FF)
            # Assign the role to the user
            await interaction.user.add_roles(role)
            count += 1

async def setup(client: commands.Bot) -> None:
    await client.add_cog(abilities(client))
