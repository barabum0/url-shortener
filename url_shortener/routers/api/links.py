import os

from fastapi import APIRouter

from url_shortener.database import create_db_client
from url_shortener.database.database import Database
from url_shortener.types.links import Link
from url_shortener.types.requests.api.links import CreateLinkRequest, CreateLinkResponse

router = APIRouter(prefix="/links", tags=["Links"])
db = Database(create_db_client())


@router.post("/create")
async def create_link(body: CreateLinkRequest) -> CreateLinkResponse:
    link = body.url.unicode_string().strip().rstrip("/")
    if existing_link := await db.Links.get_one({"origin_url": link}):
        return CreateLinkResponse(
            shortened_url=f"{os.getenv('ORIGIN_DOMAIN').rstrip('/')}/{existing_link.link_hash}",
            shortened_url_hash=existing_link.link_hash,
        )

    await db.Links.insert_one(
        Link(link_hash=await db.Links.get_unused_id(), origin_url=link)
    )
