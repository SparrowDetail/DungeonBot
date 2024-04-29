import discord
from discord.ext import commands
from discord import app_commands

import DBHelper
from DBHelper import usersDB, orderDB
from DungeonBot.cogs.Roll.dieImage import Die

def get_initiative_embed(user_id: int) -> discord.Embed:
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
        user_id: int = interaction.user.id

        try:
            if (usersDB.verify_or_add_user(user_id)):
                print("User verified...")
            else:
                print("Something went wrong!")
            
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
        try:
            user_id = interaction.user.id
            usersDB.verify_or_add_user(user_id)

            orderDB.remove_one_order(user_id, char_name)
        except Exception as e:
            print(e)
        
        try:
            embed = get_initiative_embed(user_id)
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(content="Something went wrong")
            print(e)
        
async def setup(bot: commands.Bot):
    cmd_name = "initiative"
    cmd_description = "Initiative order commands"
    bot.tree.add_command(initiative(name=cmd_name, description=cmd_description))
    print(f"Command extension: {cmd_name} added")