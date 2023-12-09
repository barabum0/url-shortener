from uuid import uuid4

from motor.core import AgnosticClient

from url_shortener.database import BaseDatabaseID
from url_shortener.types.links import Link


class Database:
    def __init__(self, client: AgnosticClient):
        self.client = client

        self.Links = BaseDatabaseID[Link](
            "links",
            self.client,
            Link,
            id_key="link_hash",
            generate_id_function=lambda: str(uuid4())[:6],
        )
