from pydantic import BaseModel, AnyHttpUrl


class CreateLinkRequest(BaseModel):
    url: AnyHttpUrl


class CreateLinkResponse(BaseModel):
    shortened_url: AnyHttpUrl
    shortened_url_hash: str
