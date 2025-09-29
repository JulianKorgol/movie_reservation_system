from pydantic import BaseModel


class PublicCountry(BaseModel):
    name: str
    url: str
