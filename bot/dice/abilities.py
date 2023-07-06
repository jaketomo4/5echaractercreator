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

    # Creates a class for the various ability buttons
    class AbilityScores(discord.ui.View):
        def __init__(self, interaction: discord.Interaction):
            super().__init__(timeout=None)

        # Creates a "Standard Array" button which is green and enabled
        @discord.ui.button(label="Standard Array", style=discord.ButtonStyle.green, disabled = False)
        async def standard_array(self, interaction: discord.Interaction, Button: discord.ui.Button):
            # Edits the original message accordingly
            await interaction.response.edit_message(content="Please select which ability you want to assign and the number you want to assign it to.", view=abilities.StandardArray(interaction))

        # Creates a "Rolling Stats" button which is green and enabled
        @discord.ui.button(label="Rolling Stats", style=discord.ButtonStyle.green, disabled = False)
        async def rolling_stats(self, interaction: discord.Interaction, Button: discord.ui.Button):
            # Edits the original message accordingly
            await interaction.response.edit_message(content="Rolling your abilities! ")

        # Creates a "Point Buy" button which is green and enabled
        @discord.ui.button(label="Point Buy", style=discord.ButtonStyle.green, disabled = False)
        async def point_buy(self, interaction: discord.Interaction, Button: discord.ui.Button):
            # Edits the original message accordingly
            await interaction.response.edit_message(content="Here is the point cost chart: ")

    # Creates a class for the Standard Array view
    class StandardArray(discord.ui.View):
        def __init__(self, interaction: discord.Interaction):
            super().__init__(timeout=None)
            self.abilities = ["Str", "Dex", "Con", "Int", "Wis", "Cha"]
            # Establish colour checks
            self.score = False
            self.number = False
            self.tracker = 0
            # Establish variables for tracking
            self.stat = ""
            self.num = ""
            # Creates a dictionary for the values
            self.standard_array = {
                "Strength": 10,
                "Dexterity": 10,
                "Consitution": 10,
                "Intelligence": 10,
                "Wisdom": 10,
                "Charisma": 10
            }

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
        @discord.ui.button(label="15", style=discord.ButtonStyle.blurple, disabled = False, row=1)
        async def fifteen(self, interaction: discord.Interaction, Button: discord.ui.Button):
            # Checks the button style, if it's one colour, change it to the other
            if Button.style == discord.ButtonStyle.blurple:
                Button.style = discord.ButtonStyle.green
                self.number = True
                self.num = Button.label
            else:
                Button.style = discord.ButtonStyle.blurple
                self.number = False
            await self.update_button(interaction, Button)
        @discord.ui.button(label="14", style=discord.ButtonStyle.blurple, disabled = False, row=2)
        async def fourteen(self, interaction: discord.Interaction, Button: discord.ui.Button):
            # Checks the button style, if it's one colour, change it to the other
            if Button.style == discord.ButtonStyle.blurple:
                Button.style = discord.ButtonStyle.green
                self.number = True
                self.num = Button.label
            else:
                Button.style = discord.ButtonStyle.blurple
                self.number = False
            await self.update_button(interaction, Button)
        @discord.ui.button(label="13", style=discord.ButtonStyle.blurple, disabled = False, row=3)
        async def thirteen(self, interaction: discord.Interaction, Button: discord.ui.Button):
            # Checks the button style, if it's one colour, change it to the other
            if Button.style == discord.ButtonStyle.blurple:
                Button.style = discord.ButtonStyle.green
                self.number = True
                self.num = Button.label
            else:
                Button.style = discord.ButtonStyle.blurple
                self.number = False
            await self.update_button(interaction, Button)
        @discord.ui.button(label="12", style=discord.ButtonStyle.blurple, disabled = False, row=1)
        async def twelve(self, interaction: discord.Interaction, Button: discord.ui.Button):
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
        async def ten(self, interaction: discord.Interaction, Button: discord.ui.Button):
            # Checks the button style, if it's one colour, change it to the other
            if Button.style == discord.ButtonStyle.blurple:
                Button.style = discord.ButtonStyle.green
                self.number = True
                self.num = Button.label
            else:
                Button.style = discord.ButtonStyle.blurple
                self.number = False
            await self.update_button(interaction, Button)
        @discord.ui.button(label="8", style=discord.ButtonStyle.blurple, disabled = False, row=3)
        async def eight(self, interaction: discord.Interaction, Button: discord.ui.Button):
            # Checks the button style, if it's one colour, change it to the other
            if Button.style == discord.ButtonStyle.blurple:
                Button.style = discord.ButtonStyle.green
                self.number = True
                self.num = Button.label
            else:
                Button.style = discord.ButtonStyle.blurple
                self.number = False
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
                        self.standard_array["Strength"] = int(self.num)
                    case "Dex":
                        self.standard_array["Dexterity"] = int(self.num)
                    case "Con":
                        self.standard_array["Constitution"] = int(self.num)
                    case "Int":
                        self.standard_array["Intelligence"] = int(self.num)
                    case "Wis":
                        self.standard_array["Wisdom"] = int(self.num)
                    case "Cha":
                        self.standard_array["Charisma"] = int(self.num)
                # Loop through the children to see which button is the selected and disable them
                for i in self.children:
                    if i.label == self.stat:
                        i.disabled = True
                        i.style = discord.ButtonStyle.gray
                    if i.label == self.num:
                        i.disabled = True
                        i.style = discord.ButtonStyle.gray
                self.score = 0
                self.number = 0
                self.tracker += 1
            
            # Checks if all the abilities have been selected
            if self.tracker == 6:
                await interaction.response.edit_message(content=f"Your ability scores have been established...", view=None)
                await abilities.dictionary_to_message(abilities, interaction, self.standard_array)
            else:
                # Edit the message with the updated view
                await interaction.response.edit_message(view=self)
        
    async def dictionary_to_message(self, interaction, dict):
        message = f"{interaction.user.mention} used the **Standard Array** and has chosen the following:\n"
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
            num = no_ws.split(":")[1]
            message = f"{message}**{abi}** : **{num}**\n"
        # Send the message
        await interaction.channel.send(f"{message}")

async def setup(client: commands.Bot) -> None:
    await client.add_cog(abilities(client))
