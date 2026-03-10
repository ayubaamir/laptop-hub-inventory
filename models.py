from pydantic import BaseModel


class Product(BaseModel):
    id: int
    name: str
    price: int
    description: str
    quantity: int = 0

    # Pydantic v2 configuration: use attributes as ORM objects
    model_config = {"from_attributes": True}
