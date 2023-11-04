from constants import *

class RatingCount:
    def __init__(self, none, bronze, silver, gold, diamond, greatOne):
        self.none = none
        self.bronze = bronze
        self.silver = silver
        self.gold = gold
        self.diamond = diamond
        self.greatOne = greatOne


def getDifficultyName(score):
    scoreIndex = -1

    for threshold in DIFFICULTY_SCORE_THRESHOLDS:
        if score >= threshold:
            scoreIndex = scoreIndex + 1
        else:
            break

    return DIFFICULTIES[scoreIndex]


def getHarvestsSinceLastDiamond(animalList):
    result = 0
    allAnimalsTemp = animalList.copy()

    allAnimals = sorted(allAnimalsTemp, key=lambda d: d.datetime, reverse=True)

    for animal in allAnimals:
        if animal.ratingIcon == 0:
            break
        result = result + 1

    return result

def getHarvestsCountTookForLastDiamond(animalList):
    result = -1
    allAnimalsTemp = animalList.copy()

    allAnimals = sorted(allAnimalsTemp, key=lambda d: d.datetime, reverse=True)

    for animal in allAnimals:
        if animal.ratingIcon == 0:
            if result == -1:
                result = 0
            else:
                break
        if result >= 0:
            result = result + 1

    if result == -1:
        result = '-'

    return result


def getRatingCounts(animalList):
    noneCount = 0
    bronzeCount = 0
    silverCount = 0
    goldCount = 0
    diamondCount = 0
    greatOneCount = 0

    for animal in animalList:
        match animal.ratingIcon:
            case 0:
                diamondCount = diamondCount + 1
            case 1:
                goldCount = goldCount + 1
            case 2:
                silverCount = silverCount + 1
            case 3:
                bronzeCount = bronzeCount + 1
            case 4:
                noneCount = noneCount + 1
            case 5:
                greatOneCount = greatOneCount + 1
            case 6:
                greatOneCount = greatOneCount + 1
            case 7:
                greatOneCount = greatOneCount + 1
            case 8:
                greatOneCount = greatOneCount + 1

    return RatingCount(noneCount, bronzeCount, silverCount, goldCount, diamondCount, greatOneCount)

