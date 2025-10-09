from pydantic import BaseModel


class PublicCinema(BaseModel):
  name: str
  city: int
  postal_code: str
  street: str
  street_number: str
  url: str
