import discord
from discord.ext import commands
from discord import app_commands

from io import BytesIO
from DungeonBot.cogs.Roll.dieImage import rollImage, RollValueAndTypeError

class Roll(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.__name = "Roll"
    
    #TODO: Move towards slash commands
    #@app_commands.command(name="Roll", description="Roll some dice")
    #async def roll(interaction: discord.Interaction):
    #    await interaction.response.send_message(content="Roll")

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Cog ready: {self.__name} initialized")
    
    @commands.command()
    async def roll(self, ctx, arg):
        try:
            numberOfDieRolled, dieType = str(arg).upper().split('D')
            filename:str = "rollImage.png"

            #Generates die image as a Byte array and the total roll value
            image_byte_array: BytesIO
            total_roll_value: int
            image_byte_array, total_roll_value = rollImage(die_max_face=int(dieType), amount_of_rolls=int(numberOfDieRolled))
            image_byte_array.seek(0)
           
            #Creates embed and sets author header and roll field
            embed = discord.Embed(color=discord.Color.dark_green())
            embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.display_avatar.url)
            embed.add_field(name=f'Roll {numberOfDieRolled}D{dieType}',value=f'**Total: {total_roll_value}**', inline=False)
            
            #Converts image byte array to a Discord file
            discord_image_file = discord.File(fp=image_byte_array, filename=filename)
            embed.set_image(url=f"attachment://{filename}")
            
            await ctx.send(file=discord_image_file, embed=embed)  
        except ValueError:
            await ctx.send(f"Roll must be entered in the form XdY, where X is the number of dice rolled and Y is a valid die type. You entered: {arg}")
        except RollValueAndTypeError as error:
            await ctx.send(error)
        except FileNotFoundError as error:
            await ctx.send(error)
        except (OSError):
            #TODO: incorporate logger - advanced setup
            await ctx.send(f'Sorry, something went wrong...')
        finally:
            image_byte_array.close()
            discord_image_file.close()

async def setup(bot: commands.Bot):
    await bot.add_cog(Roll(bot))