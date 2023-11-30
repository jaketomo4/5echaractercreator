"""
5e Character Creator
Discord Bot

Created by Jake Thompson @jaketomo4

abilities.py
"""

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
        """Slash command for abilities"""
        # Checks if the user has ability scores already
        check = await self.check_roles(interaction)
        if check:
            await interaction.response.send_message(content=f"You already have your ability scores established, would you like to reset them?", view=self.ResetAbilities(interaction), ephemeral=True)
        else:
            # Adds a view for the user to see what they can do to establish abilities
            await interaction.response.send_message(content=f"Select what you'd like to do:", view=self.AbilityScores(interaction), ephemeral=True)

    # Creates a function for checking the roles
    async def check_roles(self, interaction: discord.Interaction):
        """Check the user's roles"""
        # Assigns the user's roles to a variable
        roles = interaction.user.roles
        # Loops through the user's roles
        for role in roles:
            # Checks if it is an "ability score" role
            if role.name == "Ability Scores":
                return True
        return False
    
    # Creats a function for removing ability roles
    async def remove_roles(self, interaction: discord.Interaction):
        """Remove the user's roles"""
        # Assigns the user's roles to a variable
        roles = interaction.user.roles
        # Loops through the user's roles
        for role in roles:
            # Checks if it is an "ability score" role
            if role.name == "Ability Scores":
                # Removes it
                await interaction.user.remove_roles(role, atomic=True)

    # Creates a class for the confirmation of resetting abilities
    class ResetAbilities(discord.ui.View):
        def __init__(self, interaction: discord.Interaction):
            super().__init__(timeout=None)

        @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
        async def accept(self, interaction: discord.Interaction, Button: discord.ui.Button):
            """Accept an ability score change"""
            # If the user accepts, continue through the abilities as intended
            await interaction.response.edit_message(content=f"Select what you'd like to do:", view=abilities.AbilityScores(interaction))
            await abilities.remove_roles(abilities, interaction)

        @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
        async def decline(self, interaction: discord.Interaction, Button: discord.ui.Button):
            """Decline an ability score change"""
            await interaction.response.edit_message(content=f"Your ability scores have been unchanged.", view=None)

    # Creates a class for the various ability buttons
    class AbilityScores(discord.ui.View):
        def __init__(self, interaction: discord.Interaction):
            super().__init__(timeout=None)

        # Creates a "Standard Array" button which is green and enabled
        @discord.ui.button(label="Standard Array", style=discord.ButtonStyle.green, disabled = False)
        async def standard_array(self, interaction: discord.Interaction, Button: discord.ui.Button):
            """Create the 'Standard Array' button"""
            # Edits the original message accordingly
            await interaction.response.edit_message(content="Please select which ability you want to assign and the number you want to assign it to.", view=abilities.AbilityButtons(interaction, Button.label))

        # Creates a "Rolling Stats" button which is green and enabled
        @discord.ui.button(label="Rolling Stats", style=discord.ButtonStyle.green, disabled = False)
        async def rolling_stats(self, interaction: discord.Interaction, Button: discord.ui.Button):
            """Create the 'Rolling Stats' button"""
            # Defines the class to bypass async being used in __init__
            roll_stats = abilities.RollingStats(interaction, Button, Button.label)
            # Calls roll stats
            await roll_stats.roll_stats(interaction)

        # Creates a "Point Buy" button which is green and enabled
        @discord.ui.button(label="Point Buy", style=discord.ButtonStyle.green, disabled = False)
        async def point_buy(self, interaction: discord.Interaction, Button: discord.ui.Button):
            """Create the 'Point Buy' button"""
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
            """Create the 'Re-roll' button"""
            # Rerolls the stats
            await self.roll_stats(interaction)

        # Creates a button for the stats to be rerolled
        @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green, disabled=False)
        async def confirm(self, interaction: discord.Interaction, Button:discord.ui.Button):
            """Create the 'confirm' button"""
            # Confirms the rolled stats
            await interaction.response.edit_message(content="Please select which ability you want to assign and the number you want to assign it to.", view=abilities.AbilityButtons(interaction, Button.label, self.totals))

        async def roll_stats(self, interaction: discord.Interaction):
            """Roll the stats"""
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
            self.stat = ""
            self.ability_type = ability_type
            self.abilities = ["Str", "Dex", "Con", "Int", "Wis", "Cha"]
            self.points = 27
            # Creates a dictionary for the values
            self.default_scores = {
                "Strength": 10,
                "Dexterity": 10,
                "Constitution": 10,
                "Intelligence": 10,
                "Wisdom": 10,
                "Charisma": 10
            }

        # Creates buttons for the various stats
        @discord.ui.button(label="Str | 8", style=discord.ButtonStyle.blurple, disabled=False, row=1)
        async def str(self, interaction: discord.Interaction, Button: discord.ui.Button):
            """Create the 'Str' button"""
            # Checks the button style, if it's one colour, change it to the other
            if Button.style == discord.ButtonStyle.blurple:
                Button.style = discord.ButtonStyle.green
            else:
                Button.style = discord.ButtonStyle.blurple
            # Sets the stat to the clicked button
            self.stat = Button.label.split(" | ")[0]
            await self.update_button(interaction, Button)
        @discord.ui.button(label="Dex | 8", style=discord.ButtonStyle.blurple, disabled=False, row=2)
        async def dex(self, interaction: discord.Interaction, Button: discord.ui.Button):
            """Create the 'Dex' button"""
            # Checks the button style, if it's one colour, change it to the other
            if Button.style == discord.ButtonStyle.blurple:
                Button.style = discord.ButtonStyle.green
            else:
                Button.style = discord.ButtonStyle.blurple
            # Sets the stat to the clicked button
            self.stat = Button.label.split(" | ")[0]
            await self.update_button(interaction, Button)
        @discord.ui.button(label="Con | 8", style=discord.ButtonStyle.blurple, disabled=False, row=3)
        async def con(self, interaction: discord.Interaction, Button: discord.ui.Button):
            """Create the 'Con' button"""
            # Checks the button style, if it's one colour, change it to the other
            if Button.style == discord.ButtonStyle.blurple:
                Button.style = discord.ButtonStyle.green
            else:
                Button.style = discord.ButtonStyle.blurple
            # Sets the stat to the clicked button
            self.stat = Button.label.split(" | ")[0]
            await self.update_button(interaction, Button)
        @discord.ui.button(label="Int | 8", style=discord.ButtonStyle.blurple, disabled=False, row=1)
        async def int(self, interaction: discord.Interaction, Button: discord.ui.Button):
            """Create the 'Int' button"""
            # Checks the button style, if it's one colour, change it to the other
            if Button.style == discord.ButtonStyle.blurple:
                Button.style = discord.ButtonStyle.green
            else:
                Button.style = discord.ButtonStyle.blurple
            # Sets the stat to the clicked button
            self.stat = Button.label.split(" | ")[0]
            await self.update_button(interaction, Button)
        @discord.ui.button(label="Wis | 8", style=discord.ButtonStyle.blurple, disabled=False, row=2)
        async def wis(self, interaction: discord.Interaction, Button: discord.ui.Button):
            """Create the 'Wis' button"""
            # Checks the button style, if it's one colour, change it to the other
            if Button.style == discord.ButtonStyle.blurple:
                Button.style = discord.ButtonStyle.green
            else:
                Button.style = discord.ButtonStyle.blurple
            # Sets the stat to the clicked button
            self.stat = Button.label.split(" | ")[0]
            await self.update_button(interaction, Button)
        @discord.ui.button(label="Cha | 8", style=discord.ButtonStyle.blurple, disabled=False, row=3)
        async def cha(self, interaction: discord.Interaction, Button: discord.ui.Button):
            """Create the 'Cha' button"""
            # Checks the button style, if it's one colour, change it to the other
            if Button.style == discord.ButtonStyle.blurple:
                Button.style = discord.ButtonStyle.green
            else:
                Button.style = discord.ButtonStyle.blurple
            # Sets the stat to the clicked button
            self.stat = Button.label.split(" | ")[0]
            await self.update_button(interaction, Button)

        # Creates button for the total point
        @discord.ui.button(label="27", style=discord.ButtonStyle.grey, disabled=True, row=1)
        async def total(self, interaction: discord.Interaction, Button: discord.ui.Button):
            """Create the 'Total' button"""
            print("total")

        # Creates buttons for incrementing or decrementing
        @discord.ui.button(label="+", style=discord.ButtonStyle.green, disabled=True, row=2)
        async def plus(self, interaction: discord.Interaction, Button: discord.ui.Button):
            """Create the 'Plus' button"""
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
        @discord.ui.button(label="-", style=discord.ButtonStyle.red, disabled=True, row=3)
        async def subtract(self, interaction: discord.Interaction, Button: discord.ui.Button):
            """Create the 'Minus' button"""
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
            """Create the 'Reset' button"""
            # Loops through the buttons
            for i in self.children:
                if "|" in i.label:
                    ability_label = i.label.split(" | ")[0]
                else:
                    ability_label = i.label
                # Check if the button is an ability or a score
                if ability_label in self.abilities:
                    i.style = discord.ButtonStyle.blurple
                    # Reassign the label
                    i.label = f"{ability_label} | 8"
                    # Update the button
                if i.label == str(self.points):
                    i.label = "27"
                # Set the + and - buttons to their original state
                if i.label == "+":
                    i.disabled = True
                if i.label == "-":
                    i.disabled = False
            # Reset points
            self.points = 27
            await interaction.response.edit_message(view=self)
        
        # Creates button for reseting
        @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green, disabled=True, row=4)
        async def confirm(self, interaction: discord.Interaction, Button: discord.ui.Button):
            """Create the 'Confirm' button"""
            # Loops through the buttons
            for i in self.children:
                if "|" in i.label:
                    # Checks what ability is which and assigns accordingly
                    match (i.label.split(" | ")[0]):
                        case "Str":
                            self.default_scores["Strength"] = int(i.label.split(" | ")[1])
                        case "Dex":
                            self.default_scores["Dexterity"] = int(i.label.split(" | ")[1])
                        case "Con":
                            self.default_scores["Constitution"] = int(i.label.split(" | ")[1])
                        case "Int":
                            self.default_scores["Intelligence"] = int(i.label.split(" | ")[1])
                        case "Wis":
                            self.default_scores["Wisdom"] = int(i.label.split(" | ")[1])
                        case "Cha":
                            self.default_scores["Charisma"] = int(i.label.split(" | ")[1])
            await interaction.response.edit_message(content=f"Your ability scores have been established...", view=None)
            await abilities.dict_to_msg(abilities, interaction, self.default_scores, self.ability_type)

        # A function for updating the buttons
        async def update_button(self, interaction: discord.Interaction, Button: discord.ui.Button):
            """Update the buttons"""
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
                        # If it's not the clicked button, turn it blurple
                        if i != Button:
                            i.style = discord.ButtonStyle.blurple
            await self.update_view(interaction, Button)

        # A function for updating the view
        async def update_view(self, interaction: discord.Interaction, Button: discord.ui.Button):
            """Update the view"""
            for i in self.children:
                # Checks the selected ability
                if i.label.startswith(self.stat):
                    # Is the label selected?
                    if i.style == discord.ButtonStyle.green:
                        try:
                            score = int(i.label.split(" | ")[1])
                        except:
                            score = None
                        if score != None:
                            # Updates the + button accordingly
                            if score == 15:
                                self.children[7].disabled = True
                            else:
                                self.children[7].disabled = False
                            # Updates the - button accordingly
                            if score == 8:
                                self.children[8].disabled = True
                            else:
                                self.children[8].disabled = False
                            # Perform a check to see if the threshold is about to go over the total
                            if int(i.label.split(" | ")[1]) == 14 and self.points == 1:
                                self.children[7].disabled = True
                    else:
                        # Since the label has been deselected, set + and - to original
                        self.children[7].disabled = True
                        self.children[8].disabled = True
            # Updates the total
            self.children[6].label = f"{self.points}"
            # Updates the confirm button
            if self.points == 0:
                self.children[10].disabled = False
            else:
                self.children[10].disabled = True          
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
            """Create the 'Str' button"""
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
            """Create the 'Dex' button"""
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
            """Create the 'Con' button"""
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
            """Create the 'Int' button"""
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
            """Create the 'Wis' button"""
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
            """Create the 'Cha' button"""
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
            """Create the first ability button"""
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
            """Create the second ability button"""
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
            """Create the third ability button"""
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
            """Create the fourth ability button"""
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
            """Create the fifth ability button"""
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
            """Create the sixth ability button"""
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
            """Create the 'Reset button"""
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
            """Update the buttons"""
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
        """Convert the ability dictionary into a message"""
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
        """Assign the ability scores role"""
        # Create a string value for the colour
        clrstr = ""
        # Assign the server
        server = interaction.guild
        # Loop through the ability names
        for abi in ability:
            # Find the correct number for the abilityand convert into an integer
            num = int(number[ability.index(abi)])
            # The lowest possible ability score a user can get is 3, the highest is 18 - due to this, hexadecimal can be used, which is also for the colour assignment
            if (num >= 3) and (num <= 12):
                # Minus 3 to get the numbers equal to the first 10 hexadecimal values
                num -= 3
                # Add the number to the colour string
                clrstr += str(num)
            else:
                # Minus 12 to get the numbers to easily go from A -> F for the last 6 hexadecimal values
                num -= 12
                # Do a match-case statement to assign them to hexadecimal values
                match(num):
                    # Assign 13 to A
                    case 1:
                        # Add the hex value to the colour string
                        clrstr += "A"
                    # Assign 14 to B
                    case 2:
                        # Add the hex value to the colour string
                        clrstr += "B"
                    # Assign 15 to C
                    case 3:
                        # Add the hex value to the colour string
                        clrstr += "C"
                    # Assign 16 to D
                    case 4:
                        # Add the hex value to the colour string
                        clrstr += "D"
                    # Assign 17 to E
                    case 5:
                        # Add the hex value to the colour string
                        clrstr += "E"
                    # Assign 18 to F
                    case 6:
                        # Add the hex value to the colour string
                        clrstr += "F"
        # Add 0x to the start of the colour string
        clrstr = "0x" + clrstr
        # Turn the string into a colour using from_str
        colour = discord.Color.from_str(clrstr)
        # Assigns the server's roles to a variable
        roles = server.roles
        # Loops through the server's roles, if no break is hit, go into the else
        for role in roles:
            # Checks if it is an "ability score" role
            if role.name == "Ability Scores" and role.color == colour:
                # Assign the role to the user
                await interaction.user.add_roles(role)
                break
        else:
            # Role with matching colour hasn't been found, create role
            role = await server.create_role(name=f"Ability Scores", color=colour)
            # Assign the role to the user
            await interaction.user.add_roles(role)

    async def old_assign_roles(self, interaction: discord.Interaction, ability, number):
        """Assign the ability scores roles"""
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
    """Setup the cog"""
    await client.add_cog(abilities(client))
