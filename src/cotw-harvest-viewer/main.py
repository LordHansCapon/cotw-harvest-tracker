import pymem.exception
from reserve import *
from save import *
from pymem import Pymem
from nicegui import app, ui
from constants import *
import math
from utils import *

version = "1.16"

saveStructure = loadData()


def isDiamondHarvested(animal):
    for animalData in saveStructure.animals[animal]:
        if animalData.ratingIcon == 0:
            return True
    return False


def createAnimalGridElement(reserveName, animal, hasDiamond, harvestCount):
    with ui.link('', '/animal/'+reserveName+"/"+animal).classes('w-full'):
        with ui.card():
            with ui.image("assets/images/animals/" + animal + ".webp").style("overflow:visible"):
                ui.label(str(harvestCount)+" harvests").style("position:absolute;bottom:0;left:0;font-size:14px;padding:5px;")
                if hasDiamond:
                    ui.image("assets/images/icons/diamond-icon.png").classes('bg-transparent').style("width:40px;height:44px;position:absolute;top:-10px;right:-10px;")
            ui.label(animal).style("font-weight:600;padding-left:5px;border-left:5px solid #6683b3;")


def createAnimalDiamondCheckGridElement(animal, hasDiamond):
    with ui.link('', "/diamond-check/{animalName}".replace('{animalName}', animal)).classes('w-full'):
        with ui.card():
            with ui.image("assets/images/animals/"+animal+".webp").style("overflow:visible"):
                if hasDiamond:
                    ui.image("assets/images/icons/diamond-icon.png").classes('bg-transparent').style("width:40px;height:44px;position:absolute;top:-10px;right:-10px;")
            ui.label(animal).style("font-weight:600;padding-left:5px;border-left:5px solid #6683b3;")


def createReserveGridElement(reserveName):
    with ui.link('', '/reserve/'+reserveName).classes('w-full'):
        with ui.card():
            ui.image("assets/images/reserves/"+reserveName+".webp")
            ui.label(reserveName).style("font-weight:600;padding-left:5px;border-left:5px solid #6683b3;")


def createFooter():
    with ui.element('div').style("text-align:center;padding:15p 0;").classes("w-full"):
        ui.html("<p>Images are taken from the <b><a style='color:#6683b3' href='https://thehuntercotw.fandom.com' target='_blank'>thehuntercotw.fandom.com</a></b> wiki page.</p>").style("color:#999")
        ui.html("<p>Intended for game version: Steam default: 2649775 | Network version: 44 | 0.13.10</p>").style("color:#999")
        ui.html("<p>Visit the <b><a style='color:#6683b3' href='https://github.com/LordHansCapon/cotw-stat-viewer' target='_blank'>GitHub repo</a></b> for patch notes and latest version!</p>").style("color:#999")
        ui.html("<p>Version: "+version+"</p>").style("color:#999")


def onCellClicked(animalName, event):
    if event.args['colId'] == 'id':
        maybeOpenAnimalImage(animalName, event.args['data']['idPure'])


def getAnimalImagePath(animalName, id):
    return os.getcwd() + "/screenshots/animals/" + str(animalName) + " " + str(id) + ".png"


def maybeOpenAnimalImage(animalName, id):
    if isAnimalHasImage(animalName, id):
        os.startfile(getAnimalImagePath(animalName, id))


def isAnimalHasImage(animalName, id):
    return os.path.isfile(getAnimalImagePath(animalName, id))


@ui.page("/")
def home():
    with ui.element("div").style("display:grid;grid-template-columns:1fr auto;width:100%"):
        with ui.element("div"):
            ui.label("RESERVES").style("font-size:30px;color:#666;")
        with ui.element("div").style("text-align:right"):
            with ui.link("", "/latest").style("float:right;"):
                ui.button("LATEST HARVESTS")
            with ui.link("", "/diamond-checklist").style("float:right; margin-right: 5px"):
                ui.button("DIAMOND CHECKLIST")

    with ui.grid(columns=5).classes("w-full"):
        for reserveName in RESERVES:
            createReserveGridElement(reserveName)

    createFooter()


@ui.page("/diamond-checklist")
def reserve():
    with ui.element("div").style("display:grid;grid-template-columns:1fr auto;width:100%"):
        with ui.element("div"):
            ui.label("DIAMOND CHECKLIST").style("font-size:30px;color:#666;")
        with ui.element("div").style("text-align:right"):
            with ui.link("", "/").style("float:right;"):
                ui.button("BACK")

    animalsPerClass = []

    for animalClass in range(1, 10):
        animalsPerClass.append([])

    for reserveName in RESERVES:
        for animalClass in RESERVES[reserveName].animalsPerClass:
            for animalName in RESERVES[reserveName].animalsPerClass[animalClass]:
                if animalName not in animalsPerClass[animalClass-1]:
                    animalsPerClass[animalClass-1].append(animalName)

    maxAnimalNumber = 0
    diamondAnimalNumber = 0

    for animalClass in range(0, 9):
        if len(animalsPerClass[animalClass]) > 0:
            maxAnimalNumber = maxAnimalNumber + len(animalsPerClass[animalClass])
            for animal in animalsPerClass[animalClass]:
                if isDiamondHarvested(animal):
                    diamondAnimalNumber = diamondAnimalNumber + 1

    ui.label(str(diamondAnimalNumber)+"/"+str(maxAnimalNumber)+" diamond animals have been harvested.")

    for animalClass in range(0, 9):
        ui.label("Class "+str(animalClass+1)).style("font-size:22px;border-left:10px solid #6683b3;padding-left: 10px;")
        with ui.grid(columns=4).classes("w-full"):
            if len(animalsPerClass[animalClass]) > 0:
                for animal in animalsPerClass[animalClass]:
                    createAnimalDiamondCheckGridElement(animal, isDiamondHarvested(animal))
            else:
                ui.label("No animal in this class.")

    createFooter()


@ui.page("/latest")
def home():
    with ui.element("div").style("display:grid;grid-template-columns:1fr auto;width:100%"):
        with ui.element("div"):
            ui.label("LATEST HARVESTS").style("font-size:30px;color:#666;")
        with ui.element("div").style("text-align:right"):
            with ui.link("", "/").style("float:right;"):
                ui.button("BACK")

    ui.label("Listing the last 50 harvests")

    rowData = []
    allAnimalsTemp = []
    maxLatestAnimals = 50

    # Collect all animals into a single list
    for animalName in saveStructure.animals:
        for index, animal in enumerate(saveStructure.animals[animalName]):
            animal.type = animalName
            animal.id = index
            allAnimalsTemp.append(animal)

    allAnimals = sorted(allAnimalsTemp, key=lambda d: d.datetime, reverse=True)

    for animal in allAnimals:
        furTypeName = "UNKNOWN"

        if hasattr(animal, "furType") and animal.furType is not None:
            furTypeName = animal.furType

        if isAnimalHasImage(animal.type, animal.id):
            idDisplay = str(animal.id) + ' ⧉'
        else:
            idDisplay = str(animal.id)

        rowData.append({
            "id": idDisplay,
            "animal": animal.type,
            "gender": GENDERS[animal.gender] if GENDERS.__contains__(animal.gender) else 'UNKNOWN',
            "weight": round(animal.weight * 100) / 100,
            "badge": RATING_BADGES[animal.ratingIcon],
            "rating": math.floor(animal.rating * 100) / 100,
            "difficulty": getDifficultyName(animal.difficulty),
            "difficultyScore": math.floor(animal.difficulty * 1000) / 1000,
            "furType": furTypeName,
            "cash": animal.cash,
            "xp": animal.xp,
            "score": animal.score,
            "datetime": animal.datetime,
            'idPure': animal.id
        })

        maxLatestAnimals = maxLatestAnimals - 1
        if maxLatestAnimals == 0:
            break

    grid = ui.aggrid({
        'defaultColDef': {'sortable': True},
        'columnDefs': [
            {'headerName': 'id', 'field': 'id', 'width': '140', 'sortable': False},
            {'headerName': 'Animal', 'field': 'animal'},
            {'headerName': 'Gender', 'field': 'gender', 'width': '140'},
            {'headerName': 'Badge', 'field': 'badge', 'width': '140'},
            {'headerName': 'Rating', 'field': 'rating', 'width': '140'},
            {'headerName': 'Difficulty', 'field': 'difficulty'},
            {'headerName': 'Difficulty Score', 'field': 'difficultyScore'},
            {'headerName': 'Fur Type', 'field': 'furType'},
            {'headerName': 'Weight', 'field': 'weight', 'width': '140'},
            {'headerName': 'Cash', 'field': 'cash', 'width': '120'},
            {'headerName': 'XP', 'field': 'xp', 'width': '120'},
            {'headerName': 'Score', 'field': 'score', 'width': '120'},
            {'headerName': 'Datetime', 'field': 'datetime', 'width': '300', 'sort': 'desc'},
            {'headerName': 'idPure', 'field': 'idPure', 'hide': True},
        ],
        'pagination': True,
        'paginationPageSize': 50,
        'rowData': rowData
    }, html_columns=[0]).style("height: 600px").on('cellClicked', lambda event: onCellClicked(event.args['data']['animal'], event))

    createFooter()

@ui.page("/reserve/{reserveName}")
def reserve(reserveName):
    with ui.element("div").style("display:grid;grid-template-columns:1fr auto;width:100%"):
        with ui.element("div"):
            ui.label(reserveName).style("font-size:30px;color:#666;")
        with ui.element("div").style("text-align:right"):
            with ui.link("", "/").style("float:right;"):
                ui.button("BACK")

    for animalClass in range(1, 10):
        ui.label("Class "+str(animalClass)).style("font-size:22px;border-left:10px solid #6683b3;padding-left: 10px;")
        with ui.grid(columns=4).classes("w-full"):
            if len(RESERVES[reserveName].animalsPerClass[animalClass]) > 0:
                for animal in RESERVES[reserveName].animalsPerClass[animalClass]:
                    createAnimalGridElement(reserveName, animal, isDiamondHarvested(animal), len(saveStructure.animals[animal]))
            else:
                ui.label("No animal in this class.")

    createFooter()


@ui.page("/animal/{reserveName}/{animalName}")
def animal(reserveName, animalName):
    if animalName not in saveStructure.animals:
        saveStructure.animals[animalName] = []

    ratingCounts = getRatingCounts(saveStructure.animals[animalName])
    harvestsSinceLastDiamond = getHarvestsSinceLastDiamond(saveStructure.animals[animalName])
    harvestsCountTookForLastDiamond = getHarvestsCountTookForLastDiamond(saveStructure.animals[animalName])

    with ui.element("div").style("display:grid;grid-template-columns:1fr auto;width:100%"):
        with ui.element("div"):
            ui.label(animalName).style("font-size:30px;color:#666;")
        with ui.element("div").style("text-align:right"):
            with ui.link("", "/reserve/"+reserveName).style("float:right;"):
                ui.button("BACK")

    with ui.element("div").style("display:flex;width:100%;justify-content:space-evenly"):
        with ui.element("div"):
            ui.label("GREAT ONE: "+str(ratingCounts.greatOne))
        with ui.element("div"):
            ui.label("DIAMOND: "+str(ratingCounts.diamond))
        with ui.element("div"):
            ui.label("GOLD: "+str(ratingCounts.gold))
        with ui.element("div"):
            ui.label("SILVER: "+str(ratingCounts.silver))
        with ui.element("div"):
            ui.label("BRONZE: "+str(ratingCounts.bronze))
        with ui.element("div"):
            ui.label("NONE: "+str(ratingCounts.none))

    with ui.element("div").style("display:flex;width:100%;justify-content:space-evenly"):
        with ui.element("div"):
            ui.label("Harvests since last diamond: "+str(harvestsSinceLastDiamond))
        with ui.element("div"):
            ui.label("Harvests took for last diamond: "+str(harvestsCountTookForLastDiamond))

    allAnimalsTemp = saveStructure.animals[animalName].copy()

    rowData = []
    for index, animal in enumerate(allAnimalsTemp):
        furTypeName = "UNKNOWN"

        if hasattr(animal, "furType") and animal.furType is not None:
            furTypeName = animal.furType

        if isAnimalHasImage(animalName, index):
            idDisplay = str(index) + ' ⧉'
        else:
            idDisplay = str(index)

        rowData.append({
            "id": idDisplay,
            "gender": GENDERS[animal.gender] if GENDERS.__contains__(animal.gender) else 'UNKNOWN',
            "weight": round(animal.weight*100)/100,
            "badge": RATING_BADGES[animal.ratingIcon],
            "rating": math.floor(animal.rating*100)/100,
            "difficulty": getDifficultyName(animal.difficulty),
            "difficultyScore": math.floor(animal.difficulty*1000)/1000,
            "furType": furTypeName,
            "cash": animal.cash,
            "xp": animal.xp,
            "score": animal.score,
            "datetime": animal.datetime,
            'idPure': index
        })

    grid = ui.aggrid({
        'defaultColDef': {'sortable': True},
        'columnDefs': [
            {'headerName': 'id', 'field': 'id', 'width': '140', 'sortable': False},
            {'headerName': 'Gender', 'field': 'gender', 'width': '140'},
            {'headerName': 'Badge', 'field': 'badge', 'width': '140'},
            {'headerName': 'Rating', 'field': 'rating', 'width': '140'},
            {'headerName': 'Difficulty', 'field': 'difficulty'},
            {'headerName': 'Difficulty Score', 'field': 'difficultyScore'},
            {'headerName': 'Fur Type', 'field': 'furType'},
            {'headerName': 'Weight', 'field': 'weight', 'width': '140'},
            {'headerName': 'Cash', 'field': 'cash', 'width': '120'},
            {'headerName': 'XP', 'field': 'xp', 'width': '120'},
            {'headerName': 'Score', 'field': 'score', 'width': '120'},
            {'headerName': 'Datetime', 'field': 'datetime', 'width': '300', 'sort': 'desc'},
            {'headerName': 'idPure', 'field': 'idPure', 'hide': True},
        ],
        'pagination': True,
        'paginationPageSize': 50,
        'rowData': rowData
    }, html_columns=[0]).style("height: 600px").on('cellClicked', lambda event: onCellClicked(animalName, event))
    createFooter()


@ui.page("/diamond-check/{animalName}")
def animal(animalName):
    if animalName not in saveStructure.animals:
        saveStructure.animals[animalName] = []

    ratingCounts = getRatingCounts(saveStructure.animals[animalName])
    harvestsSinceLastDiamond = getHarvestsSinceLastDiamond(saveStructure.animals[animalName])
    harvestsCountTookForLastDiamond = getHarvestsCountTookForLastDiamond(saveStructure.animals[animalName])

    with ui.element("div").style("display:grid;grid-template-columns:1fr auto;width:100%"):
        with ui.element("div"):
            ui.label(animalName).style("font-size:30px;color:#666;")
        with ui.element("div").style("text-align:right"):
            with ui.link("", "/diamond-checklist").style("float:right;"):
                ui.button("BACK")

    with ui.element("div").style("display:flex;width:100%;justify-content:space-evenly"):
        with ui.element("div"):
            ui.label("GREAT ONE: "+str(ratingCounts.greatOne))
        with ui.element("div"):
            ui.label("DIAMOND: "+str(ratingCounts.diamond))
        with ui.element("div"):
            ui.label("GOLD: "+str(ratingCounts.gold))
        with ui.element("div"):
            ui.label("SILVER: "+str(ratingCounts.silver))
        with ui.element("div"):
            ui.label("BRONZE: "+str(ratingCounts.bronze))
        with ui.element("div"):
            ui.label("NONE: "+str(ratingCounts.none))

    with ui.element("div").style("display:flex;width:100%;justify-content:space-evenly"):
        with ui.element("div"):
            ui.label("Harvests since last diamond: "+str(harvestsSinceLastDiamond))
        with ui.element("div"):
            ui.label("Harvests took for last diamond: "+str(harvestsCountTookForLastDiamond))

    allAnimalsTemp = saveStructure.animals[animalName].copy()

    rowData = []
    for index, animal in enumerate(allAnimalsTemp):
        furTypeName = "UNKNOWN"

        if hasattr(animal, "furType") and animal.furType is not None:
            furTypeName = animal.furType

        if isAnimalHasImage(animalName, index):
            idDisplay = str(index) + ' ⧉'
        else:
            idDisplay = str(index)

        rowData.append({
            "id": idDisplay,
            "gender": GENDERS[animal.gender] if GENDERS.__contains__(animal.gender) else 'UNKNOWN',
            "weight": round(animal.weight*100)/100,
            "badge": RATING_BADGES[animal.ratingIcon],
            "rating": math.floor(animal.rating*100)/100,
            "difficulty": getDifficultyName(animal.difficulty),
            "difficultyScore": math.floor(animal.difficulty*1000)/1000,
            "furType": furTypeName,
            "cash": animal.cash,
            "xp": animal.xp,
            "score": animal.score,
            "datetime": animal.datetime,
            'idPure': index
        })

    grid = ui.aggrid({
        'defaultColDef': {'sortable': True},
        'columnDefs': [
            {'headerName': 'id', 'field': 'id', 'width': '140', 'sortable': False},
            {'headerName': 'Gender', 'field': 'gender', 'width': '140'},
            {'headerName': 'Badge', 'field': 'badge', 'width': '140'},
            {'headerName': 'Rating', 'field': 'rating', 'width': '140'},
            {'headerName': 'Difficulty', 'field': 'difficulty'},
            {'headerName': 'Difficulty Score', 'field': 'difficultyScore'},
            {'headerName': 'Fur Type', 'field': 'furType'},
            {'headerName': 'Weight', 'field': 'weight', 'width': '140'},
            {'headerName': 'Cash', 'field': 'cash', 'width': '120'},
            {'headerName': 'XP', 'field': 'xp', 'width': '120'},
            {'headerName': 'Score', 'field': 'score', 'width': '120'},
            {'headerName': 'Datetime', 'field': 'datetime', 'width': '300', 'sort': 'desc'},
            {'headerName': 'idPure', 'field': 'idPure', 'hide': True},
        ],
        'pagination': True,
        'paginationPageSize': 50,
        'rowData': rowData
    }, html_columns=[0]).style("height: 600px").on('cellClicked', lambda event: onCellClicked(animalName, event))
    createFooter()


ui.run(native=True, reload=False, window_size=(1200, 800), title="theHunterCotW: Harvest Viewer")
