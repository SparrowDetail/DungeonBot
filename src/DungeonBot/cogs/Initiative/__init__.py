import discord
from discord.ext import commands
from discord import app_commands

import DBHelper
from DBHelper import usersDB, orderDB
from DungeonBot.cogs.RNG.dieImage import Die

def get_initiative_embed(user_id: int) -> discord.Embed:
    """
    Formats and returns a discord Embed containing a target users initiative 
    order roles

    :param user_id: The target user's discord user id
    :return discord.Embed: A formatted Embed object
    """
    embed = discord.Embed(color=discord.Color.dark_green(), title="Initiative Order")
    items = orderDB.get_initiative_order(user_id)
    index = 1
    for item in items:
        r = item[1]
        m = item[2]
        embed.add_field(name=f"{index}. {item[0]}", value=f"{r+m} ({r} + {m})", inline=False)
        index = index + 1
    return embed

class initiative(app_commands.Group):
    @app_commands.command()
    async def private(self, interaction: discord.Interaction):
        """Direct message the user for private order entry"""
        try:
            msg = "Use `/interaction [add, remove, or clear]` to manage you initiative order!\n"
            msg = msg + "Use `/interaction show` to share your initiative order back in the target channel."
            await interaction.user.send(msg)
            await interaction.response.send_message("I DM'd you!")
        except Exception as e:
            await interaction.response.send_message("Something went wrong")
            print(e)
    
    @app_commands.command()
    async def show(self, interaction: discord.Interaction):
        """Display current initiative order"""
        try:
            embed = get_initiative_embed(interaction.user.id)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message("Something went wrong")
            print(e)
    
    @app_commands.command()
    async def clear(self, interaction: discord.Interaction):
        """Empty the initiative order"""
        user_id: int = interaction.user.id
        orderDB.clear_user_order(user_id)
        DBHelper.vacuum()
        await interaction.response.send_message(content="Initiative order cleared!")

    @app_commands.command()
    @app_commands.describe(
        char_name = "Character name", 
        modifier = "Roll modifier (i.e. 1 or -1)",
        roll_value = "Specify a roll value (digitally generated otherwise)",
        show = "Show the initiative order after adding"
        )
    async def add(self, interaction: discord.Interaction, char_name: str, modifier: int = 0, roll_value: int = None, show: bool = False):
        """Add a character to the initiative order"""
        user_id = interaction.user.id

        try:
            usersDB.verify_or_add_user(user_id)

            #Generate a D20 roll where roll isn't specified
            if roll_value == None:
                die: Die = Die(20)
                roll_value = die.roll()

            orderDB.add_order_command(user_id, char_name, roll_value, modifier)

            #Show the initiative embed after adding if show is True
            if show:
                embed = get_initiative_embed(user_id)
                await interaction.response.send_message(embed=embed)
            else:
                msg = f"{char_name} added: roll({roll_value}), modifier({modifier}), initiative({roll_value+modifier})"
                await interaction.response.send_message(content=msg)
        except Exception as e:
            await interaction.response.send_message("Something went wrong")
            print(e)
    
    @app_commands.command()
    @app_commands.describe(
        char_name = "Character name",
        show = "Show the initiative order after removing"
        )
    async def remove(self, interaction: discord.Interaction, char_name: str, show: bool = False):
        """Remove a character from the initiative order"""
        user_id = interaction.user.id

        try:
            usersDB.verify_or_add_user(user_id)

            if orderDB.remove_one_order(user_id, char_name):
                #Show the initiative embed after removing if show is True
                if show:
                    embed = get_initiative_embed(user_id)
                    await interaction.response.send_message(embed=embed)
                else:
                    await interaction.response.send_message(f"{char_name} removed!")
            else:
                await interaction.response.send_message(f"{char_name} does not exist")
        except Exception as e:
            await interaction.response.send_message(f"Something went wrong")
            print(e)

    @app_commands.command(description="Update a character's data")
    @app_commands.describe(
        char_name = "Character you are updating",
        change_name = "Enter a new name for the character",
        roll_value = "Manually enter a new roll value",
        auto_roll = "Generate a new roll value (overrides a manually entered value)",
        modifier = "Enter a new modifier (will also generate a new roll value)",
        show = "Show the initiative order after updating (false by default)"
    )
    async def update(self, interaction: discord.Interaction, char_name: str, change_name:str = None, roll_value: int = None, auto_roll:bool = False, modifier: int = None, show: bool = False):
        """Update a character's data"""
        user_id = interaction.user.id

        try:
            usersDB.verify_or_add_user(user_id)
            char_id = orderDB.get_character_id(user_id, char_name)

            if (char_id != None):
                if(auto_roll):
                    die:Die = Die(20)
                    roll_value = die.roll()
                if orderDB.update_character_by_id(char_id, change_name, roll_value, modifier):
                    if(show):
                        embed = get_initiative_embed(user_id)
                        await interaction.response.send_message(embed=embed)
                    else:
                        data = orderDB.get_character_by_id(char_id)
                        await interaction.response.send_message(f"Updated: name ({data[0]}), roll ({data[1]}), and modifier ({data[2]})")
                else:
                    await interaction.response.send_message(f"You must enter at least one optional value to edit {char_name}!")
            else:
                await interaction.response.send_message(f"{char_name} does not exist")
        except Exception as e:
            await interaction.response.send_message(f"Something went wrong")
            print(e)
        
async def setup(bot: commands.Bot):
    cmd_name = "initiative"
    cmd_description = "Initiative order commands"
    bot.tree.add_command(initiative(name=cmd_name, description=cmd_description))
    print(f"Command extension: {cmd_name} added")