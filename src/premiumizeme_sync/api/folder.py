from dataclasses import dataclass
from typing import List
from enum import Enum

from marshmallow import EXCLUDE


class FolderContentType(Enum):
    folder = "folder"
    file = "file"


@dataclass
class FolderContent:
    class Meta:
        unknown = EXCLUDE

    id: str
    name: str
    type: FolderContentType


@dataclass
class ListFolderResponse:
    """
    doctest: +ELLIPSIS
    >>> data = open('data.json', 'r').read()
    >>> import marshmallow_dataclass
    >>> schema = marshmallow_dataclass.class_schema(ListFolderResponse)()
    >>> res = schema.loads(data)
    >>> res.name
    'root'
    >>> len(res.content)
    75
    """
    parent_id: str
    folder_id: str
    name: str
    status: str
    content: List[FolderContent]