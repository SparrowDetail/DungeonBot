import discord
from PIL import Image
from random import randint
from io import BytesIO

ACCEPTED_DIE_TYPES: tuple = (2, 4, 6, 8, 10, 12, 20)

ASSET_WIDTH: int = 96
ASSET_HEIGHT: int = 96

ASSETS_DIRECTORY = "./Assets/"

class Die():
    def __init__(self, maxDieFace: int):
        self.__dieType = maxDieFace

    def roll(self) -> int:
        return randint(1, self.__dieType)
    
    def getDieType(self) -> int:
        return self.__dieType
    
    def setDieType(self, maxDieFace: int) -> bool:
        self.__dieType = maxDieFace
        return self.__dieType == maxDieFace

def rollImage(die_max_face: int, amount_of_rolls: int, filename: str = "image.png") -> tuple:
    """
    Generates an image containing up to four dice with random values. Returns the image as a discord file and the total rolled value as an integer.
    Raises a RollValueAndTypeError where the passed max die face is not within the accepted die types (2, 4, 6, 8, 10, 12, 20) or the amount of
    rolls is not a value from 1 to 4.

    :param die_max_face: Integer representing the max face on a typical DnD die (2, 4, 6, 8, 10, 12, 20)
    :param amount_of_rolls: Integer representing the amount of times the die will be rolled, must be between 1 and 4 (inclusive)
    :param filename: The name of the discord file being returned, 'image.png' by default
    :raise ValueError: Raised where die_max_face or amount_of_rolls is invalid
    :raise FileNotFoundError: Raised when a die asset cannot be found, must exist within Assets directory with proper naming convention ("D6_1.png")
    :return: Returns the image within a discord.File object and the calculated total of the rolls as an integer, or None where an exception is raised
    """
    #Verifies dieMaxFace and amount_of_rolls are accepted values
    if not _is_valid_type_and_roll(dieType=die_max_face, amount=amount_of_rolls):
        raise RollValueAndTypeError(f'Your roll must be a valid DnD die type {ACCEPTED_DIE_TYPES} any you may only roll up to five dice. You tried to roll: {amount_of_rolls}D{die_max_face}')

    #Roll value creation variables
    die: Die = Die(die_max_face)
    rolls: list[int] = []
    required_assets: set = set()
    
    #Generate die roll values and a set containing only the required assets
    for i in range(amount_of_rolls):
        rolls.append(die.roll())
        required_assets.add(rolls[i])
    
    #Calculated total to be returned
    total: int = sum(rolls)

    #Generation variables
    asset_X_coordinate_pointer: int = 10
    asset_y_coordinate = 0
    assets: dict = {}
    image_byte_array: BytesIO = BytesIO()
    blank: Image

    try:
        #blank base image generation variables
        asset_maximum_width: int = 0
        asset_maximum_height: int = 0

        #Pre-load all required assets and initialize asset maximum height and width values
        for i in required_assets:
            assets[i] = Image.open(f'{ASSETS_DIRECTORY}D{die_max_face}_{i}.png')
            if (assets[i].width > asset_maximum_width):
                asset_maximum_width = assets[i].width
            if (assets[i].height > asset_maximum_height):
                asset_maximum_height = assets[i].height
        
        #Generate blank image
        blank_width: int = 10
        for i in range(0, amount_of_rolls):
            blank_width = blank_width + asset_maximum_width + 10
        blank = Image.new(mode="RGBA", size=(blank_width, asset_maximum_height))
        
        #Paste each asset within the generated blank image
        for i in rolls:
            blank.paste(assets[i], (asset_X_coordinate_pointer, asset_y_coordinate))
            asset_X_coordinate_pointer = asset_X_coordinate_pointer + ASSET_WIDTH + 10
        
        #convert the image to a byte array
        blank.save(image_byte_array, format="PNG")

        return (image_byte_array, total)
    except FileNotFoundError:
        raise DieAssetNotFoundError("Sorry, a die asset appears to be missing or corrupted. Please contact your admin!")
    except Exception as e:
        print(e)
    finally:
        # Close all open class calls
        for key in assets:
            assets[key].close()
        blank.close()

def _is_valid_type_and_roll(dieType: int, amount: int) -> bool:
    """
    Validates die values are within a declared set of accepted values and within an accepted range of roll values
    """
    if dieType not in ACCEPTED_DIE_TYPES:
        return False
    if not (amount >= 1 and amount <= 5):
        return False
    return True


class RollValueAndTypeError(ValueError):
    def __init__(self, msg="Invalid die entry") -> None:
        """
        Error class used to validate key image generation factors. A RollValueAndTypeError is raised when the die type or die roll values
        don't meet the expected bounds.

        :inherit Exception:
        """
        self.msg = msg
        super().__init__(self.msg)

class DieAssetNotFoundError(FileNotFoundError):
    def __init__(self, msg="Die asset not found") -> None:
        """
        Error class used to validate die asset presence. Raised when a die asset is missing, corrupted, and/or named improperly (i.e. "D6_1.png").

        :inherit Exception:
        """
        self.msg = msg
        super().__init__(self.msg)