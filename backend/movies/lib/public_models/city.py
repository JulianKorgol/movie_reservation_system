from pydantic import BaseModel


class PublicCity(BaseModel):
  name: str
  country: int
  url: str
