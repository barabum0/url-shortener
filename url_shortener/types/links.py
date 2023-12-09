from pydantic import BaseModel, Field


class LinkStats(BaseModel):
    clicks: int = Field(ge=0, default=0)


class Link(BaseModel):
    link_hash: str
    origin_url: str

    stats: LinkStats = LinkStats()
