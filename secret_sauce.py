from typing import List
from shutil import rmtree, copyfile
from os import mkdir, path
from glob import glob

DIST_FOLDER = 'dist'

class Enigme:
    def __init__(self, *, folder: str):
        self._folder = folder

    @property
    def folder(self) -> str:
        return self._folder

    @property
    def index(self) -> str:
        return self._splits[0]

    @property
    def name(self) -> str:
        return self._splits[1]

    @property
    def answer(self) -> str:
        return self._splits[2]

    @property
    def _splits(self) -> List[str]:
        return self._folder.replace('enigmes/', '').split('_')

def get_enigmes() -> List[Enigme]:
    return sorted([Enigme(folder=folder) for folder in glob('enigmes/*')], key=lambda enigme: enigme.index)

def shift(*, enigmes: List[Enigme], by: int) -> List[Enigme]:
    for i in range(by):
        enigmes.append(enigmes.pop(0))
    return enigmes

def generate_team_filetree(*, team_index: int):
    current_dir = path.join(DIST_FOLDER, f'equipe{team_index}')
    mkdir(current_dir)
    for start_file in ['depart.html', 'dechargeDeResponsabilite.html']:
        copyfile(start_file, path.join(current_dir, start_file))
    current_dir = path.join(current_dir, 'next')
    mkdir(current_dir)
    enigmes = shift(enigmes=get_enigmes(), by=team_index - 1)
    for enigme in enigmes:
        enigme_files = glob(path.join(enigme.folder, '*'))
        for enigme_file in enigme_files:
            copyfile(enigme_file, path.join(current_dir, path.basename(enigme_file)))
        current_dir = path.join(current_dir, enigme.answer)
        mkdir(current_dir)
    copyfile('fin.html', path.join(current_dir, 'index.html'))

if __name__ == "__main__":
    try:
        rmtree(DIST_FOLDER)
    except FileNotFoundError:
        pass
    mkdir(DIST_FOLDER)
    for team_index in range(1, 11):
        generate_team_filetree(team_index=team_index)
