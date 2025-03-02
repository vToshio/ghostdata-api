from pydantic import BaseModel
from pydantic import EmailStr

class AddressSchema(BaseModel):
    number:int | str
    street_name: str
    city: str
    country: str
    postal_code: int

class UserSchema(BaseModel):
    id: int
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: int | str
    address: AddressSchema