"""
Premiumize.me API Client
"""

from typing import List, Optional
import requests
from urllib.parse import urljoin

from marshmallow_dataclass import class_schema
from premiumizeme_sync.api.folder import ListFolderResponse
from premiumizeme_sync.api.item import GetItemDetailsResponse


class PremiumizeSession(requests.Session):
    def __init__(self, apikey: str):
        super().__init__()
        self.params['apikey'] = apikey


class PremiumizeClient:
    """
    Sends requests to the Premiumize.me API.

        """
    def __init__(self, base_url: str, apikey: str):
        self._base_url = base_url
        self._session = PremiumizeSession(apikey=apikey)
        self._list_folder_response_schema = class_schema(ListFolderResponse)()
        self._get_item_details_response_schema = class_schema(
            GetItemDetailsResponse)()

    def _request(self, method: str, endpoint: str, *args,
                 **kwargs) -> requests.Response:
        """
        >>> import os
        >>> client = PremiumizeClient('https://www.premiumize.me/api/', os.getenv('PREMIUMIZEME_API_KEY'))
        >>> res = client._request('GET', 'folder/list')
        >>> res.status_code
        200
        """
        return self._session.request(method=method,
                                     url=urljoin(self._base_url, endpoint),
                                     *args,
                                     **kwargs)

    def list_folder(self, id: str = None) -> ListFolderResponse:
        """
        >>> import os
        >>> client = PremiumizeClient('https://www.premiumize.me/api/', os.getenv('PREMIUMIZEME_API_KEY'))
        >>> len(client.list_folder().content)
        75
        """
        if not id:
            params = {}
        else:
            params = {'id': id}

        res = self._request('GET', 'folder/list', params=params)
        return self._list_folder_response_schema.loads(res.text)

    def get_item_details(self, id: str) -> GetItemDetailsResponse:
        """
        >>> import os
        >>> client = PremiumizeClient('https://www.premiumize.me/api/', os.getenv('PREMIUMIZEME_API_KEY'))
        >>> client.get_item_details('j9CGWZTRb5Lzs8JbC5bLMA').link != ''
        True
        """
        res = self._request('GET', 'item/details', params={'id': id})
        return self._get_item_details_response_schema.loads(res.text)