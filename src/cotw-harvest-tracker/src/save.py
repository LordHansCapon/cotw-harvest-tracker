import os.path
import pickle


class AnimalData:
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
        return "[" + self.datetime + "] | Weight: " + str(self.weight) + " | Fur: " + str(
            self.furType) + " | Gender: " + str(self.gender) + " | Score: " + str(self.score) + " | Rating: " + str(
            self.rating) + " | Cash: " + str(self.cash) + " | XP: " + str(self.xp) + " | RatingIcon: " + str(
            self.ratingIcon) + " | Difficulty: " + str(self.difficulty) + ""

    def getID(self):
        return str(self.weight) + '-' + str(self.rating) + '-' + str(self.difficulty)


class SaveStructure:
    def __init__(self):
        self.version = "2.0"
        self.locations = {
            "HIRSCHFELDEN HUNTING RESERVE": {
                "CANADA GOOSE": [],
                "RING-NECKED PHEASANT": [],
                "RED FOX": [],
                "ROE DEER": [],
                "FALLOW DEER": [],
                "WILD BOAR": [],
                "RED DEER": [],
                "EUROPEAN RABBIT": [],
                "EUROPEAN BISON": [],
            },
            "LAYTON LAKE DISTRICT": {
                "MALLARD": [],
                "MERRIAM TURKEY": [],
                "COYOTE": [],
                "WHITE-TAILED JACKRABBIT": [],
                "BLACKTAIL DEER": [],
                "WHITETAIL DEER": [],
                "BLACK BEAR": [],
                "ROOSEVELT ELK": [],
                "MOOSE": [],
            },
            "MEDVED-TAIGA NATIONAL PARK": {
                "WESTERN CAPERCAILLIE": [],
                "SIBERIAN MUSK DEER": [],
                "EURASIAN LYNX": [],
                "WILD BOAR": [],
                "GRAY WOLF": [],
                "REINDEER": [],
                "BROWN BEAR": [],
                "MOOSE": [],
            },
            "VURHONGA SAVANNA": {
                "EURASIAN WIGEON": [],
                "SCRUB HARE": [],
                "SIDE-STRIPED JACKAL": [],
                "SPRINGBOK": [],
                "WARTHOG": [],
                "LESSER KUDU": [],
                "BLUE WILDEBEEST": [],
                "GEMSBOK": [],
                "CAPE BUFFALO": [],
                "LION": [],
            },
            "PARQUE FERNANDO": {
                "CINNAMON TEAL": [],
                "BLACKBUCK": [],
                "AXIS DEER": [],
                "COLLARED PECCARY": [],
                "PUMA": [],
                "MULE DEER": [],
                "RED DEER": [],
                "WATER BUFFALO": [],
            },
            "YUKON VALLEY NATURE RESERVE": {
                "HARLEQUIN DUCK": [],
                "RED FOX": [],
                "CANADA GOOSE": [],
                "GRAY WOLF": [],
                "CARIBOU": [],
                "MOOSE": [],
                "GRIZZLY BEAR": [],
                "PLAINS BISON": [],
            },
            "CUATRO COLINAS GAME RESERVE": {
                "RING-NECKED PHEASANT": [],
                "EUROPEAN HARE": [],
                "ROE DEER": [],
                "RONDA IBEX": [],
                "BECEITE IBEX": [],
                "GREDOS IBEX": [],
                "SOUTHEASTERN SPANISH IBEX": [],
                "IBERIAN MOUFLON": [],
                "WILD BOAR": [],
                "IBERIAN WOLF": [],
                "RED DEER": [],
            },
            "SILVER RIDGE PEAKS": {
                "MERRIAM TURKEY": [],
                "PRONGHORN": [],
                "MOUNTAIN GOAT": [],
                "BIGHORN SHEEP": [],
                "MOUNTAIN LION": [],
                "MULE DEER": [],
                "BLACK BEAR": [],
                "ROCKY MOUNTAIN ELK": [],
                "PLAINS BISON": [],
            },
            "TE AWAROA NATIONAL PARK": {
                "MERRIAM TURKEY": [],
                "MALLARD": [],
                "EUROPEAN RABBIT": [],
                "CHAMOIS": [],
                "FERAL GOAT": [],
                "SIKA DEER": [],
                "FALLOW DEER": [],
                "TAHR": [],
                "FERAL PIG": [],
                "RED DEER": [],
            },
            "RANCHO DEL ARROYO": {
                "RIO GRANDE TURKEY": [],
                "RING-NECKED PHEASANT": [],
                "ANTELOPE JACKRABBIT": [],
                "COYOTE": [],
                "MEXICAN BOBCAT": [],
                "COLLARED PECCARY": [],
                "PRONGHORN": [],
                "WHITETAIL DEER": [],
                "MULE DEER": [],
                "BIGHORN SHEEP": [],
            },
            "MISSISSIPPI ACRES PRESERVE": {
                "BOBWHITE QUAIL": [],
                "EASTERN WILD TURKEY": [],
                "GREEN-WINGED TEAL": [],
                "EASTERN COTTONTAIL RABBIT": [],
                "GRAY FOX": [],
                "COMMON RACCOON": [],
                "WHITETAIL DEER": [],
                "WILD HOG": [],
                "AMERICAN ALLIGATOR": [],
                "BLACK BEAR": [],
            },
            "REVONTULI COAST": {
                "EURASIAN WIGEON": [],
                "EURASIAN TEAL": [],
                "GOLDENEYE": [],
                "BLACK GROUSE": [],
                "HAZEL GROUSE": [],
                "MALLARD": [],
                "WESTERN CAPERCAILLIE": [],
                "TUFTED DUCK": [],
                "ROCK PTARMIGAN": [],
                "CANADA GOOSE": [],
                "WILLOW PTARMIGAN": [],
                "TUNDRA BEAN GOOSE": [],
                "MOUNTAIN HARE": [],
                "GREYLAG GOOSE": [],
                "RACCOON DOG": [],
                "EURASIAN LYNX": [],
                "WHITETAIL DEER": [],
                "BROWN BEAR": [],
                "MOOSE": [],
            },
            "NEW ENGLAND MOUNTAINS": {
                "RING-NECKED PHEASANT": [],
                "BOBWHITE QUAIL": [],
                "EASTERN WILD TURKEY": [],
                "GOLDENEYE": [],
                "MALLARD": [],
                "GREEN-WINGED TEAL": [],
                "EASTERN COTTONTAIL RABBIT": [],
                "RED FOX": [],
                "GRAY FOX": [],
                "COYOTE": [],
                "COMMON RACCOON": [],
                "BOBCAT": [],
                "WHITETAIL DEER": [],
                "BLACK BEAR": [],
                "MOOSE": [],
            },
            "EMERALD COAST AUSTRALIA": {
                "MAGPIE GOOSE": [],
                "RED FOX": [],
                "STUBBLE QUAIL": [],
                "HOG DEER": [],
                "AXIS DEER": [],
                "FERAL GOAT": [],
                "EASTERN GRAY KANGAROO": [],
                "FALLOW DEER": [],
                "FERAL PIG": [],
                "JAVAN RUSA": [],
                "RED DEER": [],
                "SAMBAR": [],
                "SALTWATER CROCODILE": [],
                "BANTENG": [],
            },
            "SUNDARPATAN HUNTING RESERVE": {
                "GREYLAG GOOSE": [],
                "WOOLLY HARE": [],
                "NORTHERN RED MUNTJAC": [],
                "TIBETAN FOX": [],
                "BLACKBUCK": [],
                "BLUE SHEEP": [],
                "SNOW LEOPARD": [],
                "TAHR": [],
                "BARASINGHA": [],
                "NILGAI": [],
                "BENGAL TIGER": [],
                "WATER BUFFALO": [],
                "WILD YAK": [],
            },
            "SALZWIESEN PARK": {
                "EURASIAN TEAL": [],
                "EURASIAN WIGEON": [],
                "TUNDRA BEAN GOOSE": [],
                "FERRUGINOUS DUCK": [],
                "GREYLAG GOOSE": [],
                "GADWALL": [],
                "EUROPEAN RABBIT": [],
                "GOLDENEYE": [],
                "MALLARD": [],
                "RING-NECKED PHEASANT": [],
                "BLACK GROUSE": [],
                "TUFTED DUCK": [],
                "COMMON RACCOON": [],
                "RACCOON DOG": [],
                "RED FOX": [],
            },
            "ASKIY RIDGE HUNTING PRESERVE": {
                "RING-NECKED PHEASANT": [],
                "CANADA GOOSE": [],
                "SNOW GOOSE": [],
                "DUSKY GROUSE": [],
                "MALLARD": [],
                "WOOD DUCK": [],
                "NORTHERN PINTAIL": [],
                "NORTH AMERICAN BEAVER": [],
                "PRONGHORN": [],
                "MOUNTAIN GOAT": [],
                "WHITETAIL DEER": [],
                "BIGHORN SHEEP": [],
                "MULE DEER": [],
                "GRAY WOLF": [],
                "WOODLAND CARIBOU": [],
                "BLACK BEAR": [],
                "MANITOBAN ELK": [],
                "MOOSE": [],
                "WOOD BISON": [],
            },
            "TÒRR NAN SÌTHEAN HUNTING ESTATE": {
                "BLACK GROUSE": [],
                "RED GROUSE": [],
                "EURASIAN WIGEON": [],
                "EURASIAN WOODCOCK": [],
                "RING-NECKED PHEASANT": [],
                "WESTERN CAPERCAILLIE": [],
                "MOUNTAIN HARE": [],
                "AMERICAN MINK": [],
                "EURASIAN PINE MARTEN": [],
                "EUROPEAN BADGER": [],
                "FERAL GOAT": [],
                "RED FOX": [],
                "FALLOW DEER": [],
                "ROE DEER": [],
                "SIKA DEER": [],
                "WILD BOAR": [],
                "RED DEER": [],
            },
        }


def saveData(saveStructure):
    f = open("harvests.sav", "wb")
    pickle.dump(saveStructure, f)
    f.close()
    return saveStructure


def transpileSaveData(saveStructure):
    defaultSaveStructure = SaveStructure()

    for locationName in defaultSaveStructure.locations:
        if locationName not in saveStructure.locations:
            saveStructure.locations[locationName] = {}

        for animalName in defaultSaveStructure.locations[locationName]:
            if animalName not in saveStructure.locations[locationName]:
                saveStructure.locations[locationName][animalName] = []

    return saveStructure


def loadData():
    if os.path.exists("harvests.sav"):
        f = open("harvests.sav", "rb")
        saveStructure = pickle.load(f)
        f.close()

        if saveStructure.version != "2.0":
            print(
                "[ERROR] harvests.sav file is version 1.x, it can not be used in 2.x! Move your harvests.sav out of the tracker\'s folder or delete it if you don\'t need it anymore. Sorry for the inconvenience.")
            input("Press Enter to close... ")
            exit(0)

        saveStructure = transpileSaveData(saveStructure)

        return saveStructure
    else:
        return saveData(SaveStructure())
