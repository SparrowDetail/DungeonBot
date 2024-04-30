import discord
from discord.ext import commands
from discord import app_commands

import DBHelper
from DBHelper import usersDB, orderDB
from DungeonBot.cogs.Roll.dieImage import Die

def get_initiative_embed(user_id: int) -> discord.Embed:
    """
    Formats and returns a discord Embed containing a target users initiative 
    order roles

    :param user_id: The target users discord user id
    :return discord.Embed: A formatted Embed object
    """
    embed = discord.Embed(color=discord.Color.dark_green(), title="Initiative Order")
    items = orderDB.get_initiative_order(user_id)
    index = 1
    for item in items:
        r = item[2]
        m = item[3]
        embed.add_field(name=f"{index}. {item[1]}", value=f"{r+m} ({r} + {m})", inline=False)
        index = index + 1
    return embed

class initiative(app_commands.Group):
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
        modifier = "Roll modifier (i.e. 1 or -1)"
        )
    async def add(self, interaction: discord.Interaction, char_name: str, modifier: int):
        """Add a character to the initiative order"""
        user_id = interaction.user.id

        try:
            usersDB.verify_or_add_user(user_id)

            die: Die = Die(20)
            roll = die.roll()
            orderDB.add_order_command(user_id, char_name, roll, modifier)

            msg = f"{char_name} added: roll({roll}), modifier({modifier}), initiative({roll+modifier})"
            await interaction.response.send_message(content=msg)
        except Exception as e:
            await interaction.response.send_message(content="Something went wrong")
            print(e)

    @app_commands.command()
    @app_commands.describe(
        char_name = "Character name", 
        modifier = "Roll modifier (i.e. 1 or -1)"
        )
    async def add_show(self, interaction: discord.Interaction, char_name: str, modifier: int):
        """Add a character to the initiative order with a modifier and show the order"""
        user_id: int = interaction.user.id

        try:
            usersDB.verify_or_add_user(user_id)
            
            die: Die = Die(20)
            orderDB.add_order_command(user_id, char_name, die.roll(), modifier)

            embed = get_initiative_embed(user_id)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            print(e)
            await interaction.response.send_message(content="Order too long")
    
    @app_commands.command()
    @app_commands.describe(
        char_name = "Character name"
        )
    async def remove(self, interaction: discord.Interaction, char_name: str):
        """Remove a character from the initiative order"""
        user_id = interaction.user.id

        try:
            usersDB.verify_or_add_user(user_id)

            if orderDB.remove_one_order(user_id, char_name):
                await interaction.response.send_message(f"{char_name} removed!")
            else:
                await interaction.response.send_message(f"{char_name} does not exist")
        except Exception as e:
            await interaction.response.send_message(f"Something went wrong")
            print(e)

    @app_commands.command()
    @app_commands.describe(
        char_name = "Character name"
        )
    async def remove_show(self, interaction: discord.Interaction, char_name: str):
        """Remove a character from the initiative order and show the order"""
        user_id = interaction.user.id

        try:
            usersDB.verify_or_add_user(user_id)

            if orderDB.remove_one_order(user_id, char_name):
                embed = get_initiative_embed(user_id)
                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message(f"{char_name} does not exist")
        except Exception as e:
            await interaction.response.send_message(f"{char_name} does not exist")
            print(e)

    @app_commands.command()
    async def show(self, interaction: discord.Interaction):
        """Display current initiative order"""
        try:
            embed = get_initiative_embed(interaction.user.id)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(content="Something went wrong")
            print(e)
    
    @app_commands.command()
    async def private(self, interaction: discord.Interaction):
        """Direct message the user for private order entry"""
        try:
            await interaction.user.send("""
                        Use `/interaction [add, remove, or clear]` to manage you initiative order!\n
                        Use `/interaction show` to share your initiative order back in the target channel.""")
            await interaction.response.send_message("I DM'd you!")
        except Exception as e:
            await interaction.response.send_message(content="Something went wrong")
            print(e)
        
async def setup(bot: commands.Bot):
    cmd_name = "initiative"
    cmd_description = "Initiative order commands"
    bot.tree.add_command(initiative(name=cmd_name, description=cmd_description))
    print(f"Command extension: {cmd_name} added")