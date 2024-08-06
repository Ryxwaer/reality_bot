from pydantic import BaseModel


class Estate(BaseModel):
    id: str
    name: str
    locality: str
    price: int
    features: str
    url: str
    scraped: str
