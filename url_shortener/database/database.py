from motor.core import AgnosticClient

from url_shortener.database import BaseDatabase
from url_shortener.types.links import Link


class Database:
    def __init__(self, client: AgnosticClient):
        self.client = client

        self.Links = BaseDatabase[Link]("links", self.client, Link)
