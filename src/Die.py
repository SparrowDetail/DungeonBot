from random import randint

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