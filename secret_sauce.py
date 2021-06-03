from typing import List
from shutil import rmtree, copyfile, copytree
from os import mkdir, path
from glob import glob

DIST_FOLDER = "dist"
START_PAGE = "depart.html"
NOT_FOUND_PAGE = "404.html"
RIDDLES_FOLDER = "enigmes"

class Riddle:
    def __init__(self, *, folder: str):
        self._folder = folder

    @property
    def folder(self) -> str:
        return self._folder

    @property
    def chapter(self) -> str:
        return self._splits[0]

    @property
    def part(self) -> str:
        return self._splits[1]

    @property
    def name(self) -> str:
        return self._splits[2]

    @property
    def answer(self) -> str:
        return self._splits[3]

    @property
    def _splits(self) -> List[str]:
        return path.basename(self._folder).split("_")

def get_riddles() -> List[Riddle]:
    return sorted([Riddle(folder=folder) for folder in glob(path.join(RIDDLES_FOLDER, "*"))], key=lambda riddle: riddle.folder)

def shift_chapter(*, riddles: List[Riddle], by: int) -> List[Riddle]:
    for _ in range(by):
        chapter = riddles[0].chapter
        while riddles[0].chapter == chapter:
            riddles.append(riddles.pop(0))
    return riddles

def generate_team_filetree(*, team_index: int):
    current_dir = path.join(DIST_FOLDER, f"equipe{team_index}")
    mkdir(current_dir)
    copyfile(START_PAGE, path.join(current_dir, START_PAGE))
    current_dir = path.join(current_dir, "next")
    mkdir(current_dir)
    riddles = shift_chapter(riddles=get_riddles(), by=team_index - 1)
    for riddle in riddles:
        riddle_files = glob(path.join(riddle.folder, "*"))
        for riddle_file in riddle_files:
            copyfile(riddle_file, path.join(current_dir, path.basename(riddle_file)))
        current_dir = path.join(current_dir, riddle.answer)
        mkdir(current_dir)
    copyfile("arrivee.html", path.join(current_dir, "index.html"))

def generate_cheat_sheet():
    lines = ["Équipes\n"]
    lines += [
        "Sport : Chaussures d’escalade, But de foot, Gants de boxe, Ballon de handball, Panier de basket\n",
        "Salle de bain : Coton-tige, Brosse à dents, Coupe-ongles, Dentifrice, Rideau de douche\n",
        "Geek : Smartphone, Ordinateur, Tablette tactile, Montre connectée, Télévision\n",
        "Instruments de musique : Saxophone, Violon, Batterie, Piano, Guitare\n",
        "Chambre : Oreiller, Matelas, Lit, Couette, Table de chevet\n",
        "Gala : Robe de soirée, Noeud papillon, Chemise, Cravate, Talons aiguille\n",
        "Alcool : Bière, Vin, Rhum, Whiskey, Vodka\n",
        "Junk food : Hamburger, Pizza, Tacos, Kebab, Hot dog\n",
        "Gastronomie française : Boeuf bourguignon, Gratin dauphinois, Cassoulet, Steak tartare, Pot au feu\n"
    ]
    lines += ["\n", "Énigmes\n"]
    lines += [f"Chapitre {riddle.chapter}, partie {riddle.part} : {riddle.answer} ({riddle.name})\n" for riddle in get_riddles()]
    with open(path.join(DIST_FOLDER, "cheatSheet.txt"), "w") as file:
        file.writelines(lines)
    
def copy_count_webapp():
    copytree('count', path.join('dist', 'count'))

if __name__ == "__main__":
    try:
        rmtree(DIST_FOLDER)
    except FileNotFoundError:
        pass
    mkdir(DIST_FOLDER)
    copyfile(NOT_FOUND_PAGE, path.join(DIST_FOLDER, NOT_FOUND_PAGE))
    for team_index in range(1, 9):
        generate_team_filetree(team_index=team_index)
    generate_cheat_sheet()
    copy_count_webapp()
