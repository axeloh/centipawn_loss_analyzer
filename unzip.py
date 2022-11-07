"""Module to extract all pgns from zip files."""

from tqdm import tqdm
import zipfile
import os

DATA_FOLDER = 'data'
OUT_FOLDER = 'data'

def unzip(path: str, delete_zip: bool = False):
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall(OUT_FOLDER)
    if delete_zip:
        os.remove(path) 

if __name__ == '__main__':
    for file in tqdm(os.listdir(DATA_FOLDER)):
        if not file.endswith('.zip'):
            continue
        unzip(f'{DATA_FOLDER}/{file}', delete_zip=True)
