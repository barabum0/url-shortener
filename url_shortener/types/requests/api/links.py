from pydantic import BaseModel, AnyHttpUrl


class CreateLinkRequest(BaseModel):
    url: AnyHttpUrl
