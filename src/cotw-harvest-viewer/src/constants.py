from location import *

LOCATIONS = {
    'HIRSCHFELDEN HUNTING RESERVE': Location(
        {
            1: ["CANADA GOOSE", "RING-NECKED PHEASANT", "EUROPEAN RABBIT"],
            2: ["RED FOX"],
            3: ["ROE DEER"],
            4: ["FALLOW DEER", "WILD BOAR"],
            5: [],
            6: ["RED DEER"],
            7: [],
            8: [],
            9: ["EUROPEAN BISON"],
        }
    ),
    'LAYTON LAKE DISTRICT': Location(
        {
            1: ["MALLARD", "MERRIAM TURKEY", "WHITE-TAILED JACKRABBIT"],
            2: ["COYOTE"],
            3: [],
            4: ["BLACKTAIL DEER", "WHITETAIL DEER"],
            5: [],
            6: [],
            7: ["BLACK BEAR"],
            8: ["ROOSEVELT ELK", "MOOSE"],
            9: [],
        }
    ),
    'MEDVED-TAIGA NATIONAL PARK': Location(
        {
            1: ["WESTERN CAPERCAILLIE"],
            2: ["SIBERIAN MUSK DEER"],
            3: ["EURASIAN LYNX"],
            4: ["WILD BOAR"],
            5: ["GRAY WOLF"],
            6: ["REINDEER"],
            7: ["BROWN BEAR"],
            8: ["MOOSE"],
            9: [],
        }
    ),
    'VURHONGA SAVANNA': Location(
        {
            1: ["EURASIAN WIGEON", "SCRUB HARE"],
            2: ["SIDE-STRIPED JACKAL"],
            3: ["SPRINGBOK"],
            4: ["WARTHOG", "LESSER KUDU"],
            5: [],
            6: ["BLUE WILDEBEEST"],
            7: [],
            8: ["GEMSBOK"],
            9: ["CAPE BUFFALO", "LION"],
        }
    ),
    'PARQUE FERNANDO': Location(
        {
            1: ["CINNAMON TEAL"],
            2: [],
            3: ["BLACKBUCK", "AXIS DEER"],
            4: ["COLLARED PECCARY"],
            5: ["PUMA"],
            6: ["MULE DEER", "RED DEER"],
            7: [],
            8: [],
            9: ["WATER BUFFALO"],
        }
    ),
    'YUKON VALLEY NATURE RESERVE': Location(
        {
            1: ["HARLEQUIN DUCK", "CANADA GOOSE"],
            2: ["RED FOX"],
            3: [],
            4: [],
            5: ["GRAY WOLF"],
            6: ["CARIBOU"],
            7: ["GRIZZLY BEAR"],
            8: ["MOOSE"],
            9: ["PLAINS BISON"],
        }
    ),
    'CUATRO COLINAS GAME RESERVE': Location(
        {
            1: ["RING-NECKED PHEASANT", "EUROPEAN HARE"],
            2: [],
            3: ["ROE DEER"],
            4: ["IBERIAN MOUFLON", "RONDA IBEX", "BECEITE IBEX", "GREDOS IBEX", "SOUTHEASTERN SPANISH IBEX",
                "WILD BOAR"],
            5: ["IBERIAN WOLF"],
            6: ["RED DEER"],
            7: [],
            8: [],
            9: [],
        }
    ),
    'SILVER RIDGE PEAKS': Location(
        {
            1: ["MERRIAM TURKEY"],
            2: [],
            3: [],
            4: ["PRONGHORN", "MOUNTAIN GOAT", "BIGHORN SHEEP"],
            5: ["MOUNTAIN LION"],
            6: ["MULE DEER"],
            7: ["BLACK BEAR"],
            8: ["ROCKY MOUNTAIN ELK"],
            9: ["PLAINS BISON"],
        }
    ),
    'TE AWAROA NATIONAL PARK': Location(
        {
            1: ["MERRIAM TURKEY", "MALLARD", "EUROPEAN RABBIT"],
            2: [],
            3: ["CHAMOIS", "FERAL GOAT"],
            4: ["SIKA DEER", "FALLOW DEER", "FERAL PIG"],
            5: [],
            6: ["RED DEER"],
            7: [],
            8: [],
            9: [],
        }
    ),
    'RANCHO DEL ARROYO': Location(
        {
            1: ["RIO GRANDE TURKEY", "RING-NECKED PHEASANT", "ANTELOPE JACKRABBIT"],
            2: ["COYOTE"],
            3: ["MEXICAN BOBCAT"],
            4: ["COLLARED PECCARY", "BIGHORN SHEEP", "WHITETAIL DEER", "PRONGHORN"],
            5: [],
            6: ["MULE DEER"],
            7: [],
            8: [],
            9: [],
        }
    ),
    'MISSISSIPPI ACRES PRESERVE': Location(
        {
            1: ["BOBWHITE QUAIL", "EASTERN WILD TURKEY", "GREEN-WINGED TEAL", "EASTERN COTTONTAIL RABBIT"],
            2: ["GRAY FOX", "COMMON RACCOON"],
            3: [],
            4: ["WHITETAIL DEER", "WILD HOG"],
            5: [],
            6: ["AMERICAN ALLIGATOR"],
            7: ["BLACK BEAR"],
            8: [],
            9: [],
        }
    ),
    'REVONTULI COAST': Location(
        {
            1: ["EURASIAN WIGEON", "EURASIAN TEAL", "GOLDENEYE", "MALLARD", "TUFTED DUCK", "CANADA GOOSE",
                "GREYLAG GOOSE", "TUNDRA BEAN GOOSE", "BLACK GROUSE", "HAZEL GROUSE", "WESTERN CAPERCAILLIE",
                "ROCK PTARMIGAN", "WILLOW PTARMIGAN", "MOUNTAIN HARE"],
            2: ["RACCOON DOG"],
            3: ["EURASIAN LYNX"],
            4: ["WHITETAIL DEER"],
            5: [],
            6: [],
            7: ["BROWN BEAR"],
            8: ["MOOSE"],
            9: [],
        }
    ),
    'NEW ENGLAND MOUNTAINS': Location(
        {
            1: ["RING-NECKED PHEASANT", "BOBWHITE QUAIL", "EASTERN WILD TURKEY", "GOLDENEYE", "MALLARD",
                "GREEN-WINGED TEAL", "EASTERN COTTONTAIL RABBIT"],
            2: ["RED FOX", "GRAY FOX", "COYOTE", "COMMON RACCOON"],
            3: ["BOBCAT"],
            4: ["WHITETAIL DEER"],
            5: [],
            6: [],
            7: ["BLACK BEAR"],
            8: ["MOOSE"],
            9: [],
        }
    ),
    'EMERALD COAST AUSTRALIA': Location(
        {
            1: ["MAGPIE GOOSE", "STUBBLE QUAIL"],
            2: ["RED FOX"],
            3: ["HOG DEER", "AXIS DEER", "FERAL GOAT"],
            4: ["EASTERN GRAY KANGAROO", "FALLOW DEER", "FERAL PIG"],
            5: [],
            6: ["RED DEER", "SAMBAR", "JAVAN RUSA"],
            7: ["SALTWATER CROCODILE"],
            8: [],
            9: ["BANTENG"],
        }
    ),
    'SUNDARPATAN HUNTING RESERVE': Location(
        {
            1: ["GREYLAG GOOSE", "WOOLLY HARE"],
            2: ["NORTHERN RED MUNTJAC", "TIBETAN FOX"],
            3: ["BLACKBUCK"],
            4: ["SNOW LEOPARD", "BLUE SHEEP", "TAHR"],
            5: [],
            6: ["BARASINGHA", "NILGAI"],
            7: [],
            8: [],
            9: ["BENGAL TIGER", "WATER BUFFALO", "WILD YAK"],
        }
    ),
    "SALZWIESEN PARK": Location(
        {
            1: ["EURASIAN TEAL", "EURASIAN WIGEON", "TUNDRA BEAN GOOSE", "FERRUGINOUS DUCK", "GREYLAG GOOSE", "GADWALL",
                "EUROPEAN RABBIT", "GOLDENEYE", "MALLARD", "RING-NECKED PHEASANT", "BLACK GROUSE", "TUFTED DUCK"],
            2: ["COMMON RACCOON", "RACCOON DOG", "RED FOX"],
            3: [],
            4: [],
            5: [],
            6: [],
            7: [],
            8: [],
            9: [],
        }
    ),
    "ASKIY RIDGE HUNTING PRESERVE": Location(
        {
            1: ["RING-NECKED PHEASANT", "CANADA GOOSE", "SNOW GOOSE", "DUSKY GROUSE", "MALLARD", "WOOD DUCK",
                "NORTHERN PINTAIL"],
            2: ["NORTH AMERICAN BEAVER"],
            3: ["PRONGHORN"],
            4: ["MOUNTAIN GOAT", "WHITETAIL DEER"],
            5: ["BIGHORN SHEEP", "MULE DEER"],
            6: ["GRAY WOLF", "WOODLAND CARIBOU"],
            7: ["BLACK BEAR", "MANITOBAN ELK"],
            8: ["MOOSE"],
            9: ["WOOD BISON"],
        }
    ),
    "TÒRR NAN SÌTHEAN HUNTING ESTATE": Location(
        {
            1: ["BLACK GROUSE", "RED GROUSE", "EURASIAN WIGEON", "EURASIAN WOODCOCK", "RING-NECKED PHEASANT",
                "WESTERN CAPERCAILLIE", "MOUNTAIN HARE", "AMERICAN MINK", "EURASIAN PINE MARTEN"],
            2: ["EUROPEAN BADGER", 'RED FOX'],
            3: ["FERAL GOAT", "ROE DEER"],
            4: ["FALLOW DEER", "SIKA DEER"],
            5: ["WILD BOAR"],
            6: ["RED DEER"],
            7: [],
            8: [],
            9: [],
        }
    )
}

GENDERS = {
    1: "MALE",
    2: "FEMALE"
}

RATING_BADGES = {
    0: "DIAMOND",
    1: "GOLD",
    2: "SILVER",
    3: "BRONZE",
    4: "NONE",
    5: "GREAT ONE",
    6: "GREAT ONE",
    7: "GREAT ONE",
    8: "GREAT ONE"
}

DIFFICULTY_SCORE_THRESHOLDS = [0, 0.115, 0.225, 0.335, 0.445, 0.555, 0.665, 0.775, 0.885]

DIFFICULTIES = {
    0: "TRIVIAL",
    1: "MINOR",
    2: "VERY EASY",
    3: "EASY",
    4: "MEDIUM",
    5: "HARD",
    6: "VERY HARD",
    7: "MYTHICAL",
    8: "LEGENDARY",
    9: "FABLED",
}
