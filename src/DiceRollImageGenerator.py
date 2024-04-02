from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from random import randint

class BoundedImage():
    def __init__(self, dieType: int, rollCount: int) -> None:
        """
        Generator class for creating a roll image with predefined bounds (434px by 204px). Accepts a traditional table-top
        rpg die type (D2, D4, D6, D8, D10, D12, and D20) and generates roll values for up to four rolls. The final image
        will display a roll indicator (ex: "Roll 3D20"), followed by the generated die roll assets, and lastly a calculated
        total die value (ex: "Total: 23").

        :param dieType: integer representing the max face value of a traditional table-top rpg die type (D2, D4, D6, D8, D10, D12, and D20)
        :param rollCount: integer representing the amount of dice to be rolled. Must be a value of 1 to 4
        :exception RollValueAndTypeError: raised when the rollCount or dieType are outside the accepted values 
        :exception FileNotFoundError: raised when a die asset cannot be found within the Assets/ directory (ex: Assets/D6_1.png)
        :exception OSError: raised when the target font cannot be found in the Fonts directory
        """
        self.acceptedDieTypes: tuple = (2, 4, 6, 8, 10, 12, 20)
        self.dieType = self._is_valid_dieType(dieType)
        self.rollCount = self._is_valid_roll_count(rollCount)
        self.imageBounds = (434, 204)
        self.imageFont = self._get_image_font()
        self.rollValues = self._create_roll_values()
        self.die_assets = self._get_required_assets()
        self.image = self._generate_die_image()
    
    def __str__(self) -> str:
        """
        :return: string representation of object
        """
        return f"Rolled {self.rollCount}D{self.dieType}: {str(self.rollValues)}"
    
    def _is_valid_dieType(self, dieType: int) -> int:
        """
        Validates the passed dieType as an accepted value (2, 4, 6, 8, 10, 12, 20) 

        :param dieType: dieType to be validated
        :return: Returns dieType if valid, else raises a RollValueAndTypeError
        :exception RollValueAndTypeError: raised when dieType is not an accepted value (2, 4, 6, 8, 10, 12, 20)
        """
        if dieType in self.acceptedDieTypes:
            return dieType
        else: 
            raise RollValueAndTypeError(f"Invalid die type passed: D{dieType} not accepted")
    
    def _is_valid_roll_count(self, rollCount: int) -> int:
        """
        Validates the passed rollCount as a valid value (1 to 4)

        :param rollCount: rollCount to be validated
        :return: Returns rollCount if valid, else raises a RollValueAndTypeError
        :exception RollValueAndTypeError: raised when rollCount is not an accepted value
        """
        if rollCount >= 1 and rollCount <= 4:
            return rollCount
        else:
            raise RollValueAndTypeError(f"Invalid roll count passed. May only roll 1 to 4 die: {rollCount} passed")
    
    def _get_image_font(self):
        """
        Accesses and returns Mitr TrueTypeFont from the Fonts directory

        :exception OSError: raised when target font is missing, target directory "./Fonts/Mitr/Mitr-Regular.ttf"
        """
        try:
            font = ImageFont.truetype("./Fonts/Mitr/Mitr-Regular.ttf", 32)
            return font
        except OSError:
            OSError("Font not detected")
    
    def _create_roll_values(self) -> list:
        """
        Generates random roll values based on the BoundImage dieType and rollCount values. Random values are stored as a
        list of integers with a value of 1 to dieType.

        :return: list of integers representing generated roll values
        """
        rolls:list = []

        for i in range(0,self.rollCount):
            rolls.append(randint(1,self.dieType))

        return rolls
    
    def _get_required_assets(self) -> dict:
        """
        Initializes required die assets based on BoundImage rollValues. Assets returned as a dictionary with key values corresponding to
        the rollValues pointing to DieAsset objects containing the target die assets.

        :return: dictionary of rollValue and DieAsset pairs
        """
        requiredRollAssets = set()
        assets: dict = {}

        for i in self.rollValues:
            requiredRollAssets.add(i)
        
        for j in requiredRollAssets:
            assets[j] = DieAsset(self.dieType, j)
                       
        return assets
    
    def _generate_die_image(self) -> Image:
        """
        Generates a formatted image with pre-defined bounds based on the BoundImage attributes

        :return: PIL.Image object containing the generated image
        """
        baseImage = Image.new(mode="RGBA", size=self.imageBounds)
        textColor = (255, 255, 255)
        
        rollTypeHeaderText = f"Roll {self.rollCount}D{self.dieType}"
        rollTotalFooterText = f"Total: {sum(self.rollValues)}"
        
        #Starting, non-relative coordinates
        header_Y_coordinate = 5
        asset_X_coordinate_pointer = 10

        textGraphicCreator = ImageDraw.Draw(baseImage)

        #Get header and footer bounds used for relative positioning
        _, _, headerRight, headerBottom = textGraphicCreator.textbbox((0,0), text=rollTypeHeaderText, font=self.imageFont)
        _, _, footerRight, _ = textGraphicCreator.textbbox((0,0), text=rollTotalFooterText, font=self.imageFont)

        #Calculate relative coordinates for image header and image assets
        #image footer Y coordinate will be calculated based on the maximum asset height
        header_centered_X_coordinate = (self.imageBounds[0] - headerRight) / 2
        footer_centered_X_coordinate = (self.imageBounds[0] - footerRight) / 2
        asset_Y_coordinate = header_Y_coordinate + headerBottom + 10

        #Draws image header text
        textGraphicCreator.text((header_centered_X_coordinate, header_Y_coordinate), rollTypeHeaderText, font=self.imageFont, fill=textColor)

        #Paste asset images into the baseImage, assetsMaxHeight used in footer y coordinate calculation
        assetsMaxHeight = 0
        for i in self.rollValues:
            baseImage.paste(self.die_assets[i].getImage(), (asset_X_coordinate_pointer, asset_Y_coordinate))
            asset_X_coordinate_pointer += self.die_assets[i].getWidth() + 10

            if assetsMaxHeight < self.die_assets[i].getHeight():
                assetsMaxHeight = self.die_assets[i].getWidth()
        
        #Calculate footer Y coordinate and draw
        footer_Y_coordinate = asset_Y_coordinate + assetsMaxHeight + 10
        textGraphicCreator.text((footer_centered_X_coordinate, footer_Y_coordinate), rollTotalFooterText, font=self.imageFont, fill=textColor)

        return baseImage
    
    def getImage(self) -> Image:
        """
        Returns a generated image based on the BoundImage dieType and rollCount.

        :return: BoundImage.image
        """
        return self.image
    
    def getByteArray(self):
        """
        Converts the BoundImage to a Byte array and returns the Byte array as a BytesIO object

        :return: io.ByteIO object containing BoundImage Byte array
        """
        byteArray = BytesIO()
        self.image.save(byteArray, format="PNG")
        return byteArray
    
    def save(self, filePath: str):
        """
        Saves the generated BoundImage to a passed file path (ex: "./ImageSaves/example.png").

        :param filePath: target file path for saved image
        """
        self.image.save(fp=filePath)
        return True
    
    def close(self):
        for i in self.die_assets:
            self.die_assets[i].close()
        self.image.close()
        pass




class DieAsset():
    def __init__(self, dieType:int, rollValue:int) -> None:
        """
        Container class for die assets. All assets must exist within the Assets directory and must meet naming convention
        of "D{dieType}_{rollValue}.png" (ex: "./Assets/D6_1.png").

        :param dieType: Maximum face value on the DieAsset
        :param rollValue: The face rolled on the DieAsset
        :exception FileNotFoundError: raised when the target die asset is missing from the Assets directory
        """
        self.dieType = dieType
        self.rollValue = rollValue
        self.image_asset = self._open_die_asset()
    
    def __str__(self) -> str:
        """
        :return: string representation of object
        """
        return f"D{self.dieType}_{self.rollValue}.png"
    
    def _open_die_asset(self) -> Image:
        """
        Attempts to open the target die asset from within the Assets directory.

        :exception FileNotFoundError: raised when the target die asset is missing from the Assets directory (must meet standard naming convention 
        "D{dieType}_{rollValue}.png").
        """
        try:
            assetImage = Image.open(f"./Assets/D{self.dieType}_{self.rollValue}.png")
            return assetImage
        except FileNotFoundError:
            FileNotFoundError(f"Requested file was not found in the Assets directory: D{self.dieType}_{self.rollValue}.png")

    def getImage(self) -> Image:
        """
        Returns the DieAsset image file

        :return: DieAsset.image_asset
        """
        return self.image_asset
    
    def getWidth(self) -> float:
        """
        Returns the DieAsset image width in pixels

        :return: DieAsset width
        """
        return self.image_asset._size[0]
    
    def getHeight(self):
        """
        Returns the DieAsset image height in pixels

        :return: DieAsset height
        """
        return self.image_asset._size[1]
    
    def close(self):
        self.image_asset.close()
        pass

class RollValueAndTypeError(Exception):
    def __init__(self, msg="Invalid die entry") -> None:
        """
        Error class used to validate key image generation factors. A RollValueAndTypeError is raised when the die type or die roll values
        don't meet the expected bounds.

        :inherit Exception:
        """
        self.msg = msg
        super().__init__(self.msg)
