from dataclasses import dataclass

from marshmallow import EXCLUDE


@dataclass
class GetItemDetailsResponse:
    class Meta:
        unknown = EXCLUDE

    id: str
    name: str
    link: str