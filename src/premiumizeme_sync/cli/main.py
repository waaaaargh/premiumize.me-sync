import os
from typing import Optional
from dataclasses import dataclass
import shutil

import requests
from fire import Fire
from marshmallow import base

from premiumizeme_sync.api.client import PremiumizeClient
from premiumizeme_sync.api.folder import FolderContentType
from premiumizeme_sync.api.item import GetItemDetailsResponse


@dataclass
class Folder:
    id: str
    name: str


@dataclass
class File:
    id: str
    name: str


def sync(target: str, folder_id: str):
    client = PremiumizeClient(base_url=os.getenv('PREMIUMIZEME_ENDPOINT'),
                              apikey=os.getenv('PREMIUMIZEME_API_KEY'))

    remaining_folders = [Folder(id=folder_id, name='.')]

    found_files = []

    while remaining_folders:
        current_folder = remaining_folders.pop(0)
        res = client.list_folder(current_folder.id)
        for item in res.content:
            if item.type == FolderContentType.folder:
                remaining_folders.append(
                    Folder(id=item.id,
                           name=f"{current_folder.name}/{item.name}"))
            elif item.type == FolderContentType.file:
                found_files.append(
                    File(id=item.id,
                         name=f"{current_folder.name}/{item.name}"))

    for file in found_files:
        local_path = os.path.join(target, file.name)
        if os.path.isfile(local_path):
            continue

        file_details = client.get_item_details(file.id)

        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        with open(local_path, 'wb') as local_file:
            print(f"downloading file {file.name}")
            res = requests.get(file_details.link, stream=True)
            for chunk in res.iter_content(chunk_size=1024000):
                if chunk:
                    local_file.write(chunk)


def main():
    Fire(sync)