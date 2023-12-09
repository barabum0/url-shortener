from fastapi import APIRouter

from url_shortener.database import create_db_client
from url_shortener.database.database import Database

router = APIRouter(prefix="/links", tags=["Links"])
db = Database(create_db_client())
