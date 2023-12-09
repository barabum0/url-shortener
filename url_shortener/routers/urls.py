from fastapi import APIRouter, Path, HTTPException
from starlette.responses import RedirectResponse

from url_shortener.database import create_db_client
from url_shortener.database.database import Database

router = APIRouter(prefix="", tags=["URLs"])
db = Database(create_db_client())


@router.get("/{url_hash}", status_code=307, response_class=RedirectResponse)
async def redirect_url(url_hash: str = Path()):
    link = await db.Links.get_one_id(url_hash)
    if not link:
        raise HTTPException(status_code=404, detail="Link not found")

    return RedirectResponse(url=link.origin_url)
