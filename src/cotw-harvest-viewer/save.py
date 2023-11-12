import os.path
import pickle


class AnimalData:
    type: ""

    def __init__(self, weight, gender, score, rating, cash, xp, ratingIcon, difficulty, datetime, furType):
        self.weight = weight
        self.gender = gender
        self.score = score
        self.rating = rating
        self.cash = cash
        self.xp = xp
        self.ratingIcon = ratingIcon
        self.difficulty = difficulty
        self.datetime = datetime
        self.furType = furType

    def toString(self):
        return "["+self.datetime+"] | Weight: "+str(self.weight)+" | Fur: "+str(self.furType)+" | Gender: "+str(self.gender)+" | Score: "+str(self.score)+" | Rating: "+str(self.rating)+" | Cash: "+str(self.cash)+" | XP: "+str(self.xp)+" | RatingIcon: "+str(self.ratingIcon)+" | Difficulty: "+str(self.difficulty)+""

    def getID(self):
        return str(self.weight)+'-'+str(self.rating)+'-'+str(self.difficulty)

class SaveStructure:
    def __init__(self):
        self.version = "1.0"
        self.animals = {
            "AMERICAN ALLIGATOR": [],
            "ANTELOPE JACKRABBIT": [],
            "AXIS DEER": [],
            "BANTENG": [],
            "BECEITE IBEX": [],
            "BIGHORN SHEEP": [],
            "BLACK BEAR": [],
            "BLACK GROUSE": [],
            "BLACKBUCK": [],
            "BLACKTAIL DEER": [],
            "BLUE WILDEBEEST": [],
            "BOBWHITE QUAIL": [],
            "CANADA GOOSE": [],
            "CAPE BUFFALO": [],
            "CARIBOU": [],
            "CHAMOIS": [],
            "CINNAMON TEAL": [],
            "COLLARED PECCARY": [],
            "COMMON RACCOON": [],
            "COYOTE": [],
            "EASTERN COTTONTAIL RABBIT": [],
            "EASTERN GRAY KANGAROO": [],
            "EASTERN WILD TURKEY": [],
            "BROWN BEAR": [],
            "EURASIAN LYNX": [],
            "EURASIAN TEAL": [],
            "EURASIAN WIGEON": [],
            "EUROPEAN BISON": [],
            "EUROPEAN HARE": [],
            "EUROPEAN RABBIT": [],
            "FALLOW DEER": [],
            "FERAL GOAT": [],
            "FERAL PIG": [],
            "GEMSBOK": [],
            "GOLDENEYE": [],
            "GRAY FOX": [],
            "GRAY WOLF": [],
            "GREDOS IBEX": [],
            "GREEN-WINGED TEAL": [],
            "GREYLAG GOOSE": [],
            "GRIZZLY BEAR": [],
            "HARLEQUIN DUCK": [],
            "HAZEL GROUSE": [],
            "HOG DEER": [],
            "IBERIAN MOUFLON": [],
            "IBERIAN WOLF": [],
            "JAVAN RUSA": [],
            "LESSER KUDU": [],
            "LION": [],
            "MAGPIE GOOSE": [],
            "MALLARD": [],
            "MERRIAM TURKEY": [],
            "MEXICAN BOBCAT": [],
            "MOOSE": [],
            "MOUNTAIN GOAT": [],
            "MOUNTAIN HARE": [],
            "MOUNTAIN LION": [],
            "MULE DEER": [],
            "PLAINS BISON": [],
            "PRONGHORN": [],
            "PUMA": [],
            "RACCOON DOG": [],
            "RED DEER": [],
            "RED FOX": [],
            "REINDEER": [],
            "RING-NECKED PHEASANT": [],
            "RIO GRANDE TURKEY": [],
            "ROCK PTARMIGAN": [],
            "ROCKY MOUNTAIN ELK": [],
            "ROE DEER": [],
            "RONDA IBEX": [],
            "ROOSEVELT ELK": [],
            "SALTWATER CROCODILE": [],
            "SAMBAR": [],
            "SCRUB HARE": [],
            "SIBERIAN MUSK DEER": [],
            "SIDE-STRIPED JACKAL": [],
            "SIKA DEER": [],
            "SOUTHEASTERN SPANISH IBEX": [],
            "SPRINGBOK": [],
            "STUBBLE QUAIL": [],
            "TUFTED DUCK": [],
            "TUNDRA BEAN GOOSE": [],
            "WARTHOG": [],
            "WATER BUFFALO": [],
            "WESTERN CAPERCAILLIE": [],
            "WHITE-TAILED JACKRABBIT": [],
            "WHITETAIL DEER": [],
            "WILD BOAR": [],
            "WILD HOG": [],
            "WILLOW PTARMIGAN": [],
            "BOBCAT": []
        }


def saveData(saveStructure):
    f = open("harvests.sav", "wb")
    pickle.dump(saveStructure, f)
    f.close()
    return saveStructure


def transpileSaveData(saveStructure):
    defaultSaveStructure = SaveStructure()

    for animalName in defaultSaveStructure.animals:
        if animalName not in saveStructure.animals:
            saveStructure.animals[animalName] = []

    return saveStructure


def loadData():
    if os.path.exists("harvests.sav"):
        f = open("harvests.sav", "rb")
        saveStructure = pickle.load(f)
        f.close()

        saveStructure = transpileSaveData(saveStructure)

        return saveStructure
    else:
        return saveData(SaveStructure())

