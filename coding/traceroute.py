# TCP traceroute
from typing import List
from urllib3.util import Url
import requests import socket


def traceroute_location(
    url: str | Url,
    min_hops: int = 0,
    max_hops: int = 30,
):
    locations: List[str] = []
    if isinstance(url, str):
        url = Url(url)

    for i in range(min_hops, max_hops):
        requests.get()
        pass
