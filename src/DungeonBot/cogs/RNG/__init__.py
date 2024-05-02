import discord
from discord.ext import commands
from discord import app_commands

from io import BytesIO
from DungeonBot.cogs.RNG.dieImage import rollImage, Die, ACCEPTED_DIE_TYPES

class RNG(app_commands.Group):
    @app_commands.command()
    @app_commands.describe(
        die_type = f"Roll a die {ACCEPTED_DIE_TYPES}",
        amount = "Number of die to roll (1 to 4)"
    )
    async def roll(self, interaction: discord.Interaction, die_type: int, amount: int):
        """Roll an existing die up to five times"""
        try:
            filename:str = "rollImage.png"

            #Generates die image as a Byte array and the total roll value
            image_byte_array: BytesIO
            total_roll_value: int
            image_byte_array, total_roll_value = rollImage(die_max_face=die_type, amount_of_rolls=amount)
            image_byte_array.seek(0)
           
            #Creates embed and sets author header and roll field
            embed = discord.Embed(color=discord.Color.dark_green())
            embed.set_author(name=interaction.user.display_name, icon_url=interaction.user.display_avatar.url)
            embed.add_field(name=f'Roll: {amount}D{die_type}',value=f'**Total: {total_roll_value}**', inline=False)
            
            #Converts image byte array to a Discord file
            discord_image_file = discord.File(fp=image_byte_array, filename=filename)
            embed.set_image(url=f"attachment://{filename}")
            
            await interaction.response.send_message(file=discord_image_file, embed=embed)  
        except ValueError as error:
            await interaction.response.send_message(error)
        except FileNotFoundError as error:
            await interaction.response.send_message(error)
        except (OSError):
            await interaction.response.send_message(f'Sorry, something went wrong...')
        finally:
            image_byte_array.close()
            discord_image_file.close()
    
    @app_commands.command()
    @app_commands.describe(
        head = "Max value (i.e. '100' will generate a number 1 to 100)",
        amount = "Amount of values to generate (1 to 25)"
    )
    async def random(self, interaction: discord.Interaction, head: int, amount: int):
        """Generate 1 to 25 random numbers of any size"""
        try:
            if not (amount >= 1 and amount <= 25):
                await interaction.response.send_message("I can only generate 1 to 25 random values!")
                return
            if not head > 0:
                await interaction.response.send_message("Head must be a positive integer greater than 0")
                return
            
            die: Die = Die(head)
            embed = discord.Embed(title="Random values", color=discord.Color.dark_green())
            msg = ""

            for i in range(1, amount + 1):
                msg = msg + f"**{i}.** {die.roll()}\n"
            embed.add_field(name=f"Values:", value=msg,inline=False)
            
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            interaction.response.send_message("Something went wrong")
            print(e)

async def setup(bot: commands.Bot):
    cmd_name = "rng"
    cmd_description = "Random number generation commands"
    bot.tree.add_command(RNG(name=cmd_name, description=cmd_description))
    print(f"Command extension: {cmd_name} added")