from fastapi.exceptions import HTTPException
from .base_generator import Generator
from src.schemas.user_schemas import *
from faker import Faker
import asyncio


class UserGenerator(Generator):
    _instances = {}

    def _generate_email(first:str, last:str, safe:bool, fake:Faker):
        '''
        Gera um e-mail seguro (ou não) de acordo com o primeiro e último nome de uma pessoa
        '''
        email = f'{first.lower().replace(" ", "")}.{last.lower().replace(" ", "")}@{fake.safe_domain_name() if safe else fake.domain_name()}'
        return email

    @classmethod
    def get_instance(cls, locale:str='pt-BR') -> Faker:
        if locale not in cls._instances.keys():
            cls._instances[locale] = Faker(locale=locale)
        return cls._instances.get(locale, 'pt-BR')
    
    @classmethod
    def _generate_sync(cls, fake:Faker, gender:str='any', safe:bool=True):
        try:
            gender = gender.lower()

            if gender not in ['f', 'm', 'any']:
                raise KeyError("'gender' parameter should be 'm', 'f' or 'any'")
            
            genders = {
                'f': fake.first_name_female,
                'm': fake.first_name_male,
                'any': fake.first_name,
            }

            first = genders[gender]()
            last = fake.last_name()
            email = cls._generate_email(first, last, safe, fake)

            data = UserSchema(
                id = fake.random_int(),
                first_name = first,
                last_name = last,
                email = email,
                phone_number = fake.phone_number(),
                address = AddressSchema(
                    number = fake.building_number(),
                    street_name = fake.street_name(),
                    city = fake.city(),
                    country = fake.country(),
                    postal_code = fake.postcode()
                )
            )

            return data
        except KeyError as err:
            raise HTTPException(status_code=400, detail=str(err))
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))
    
    @classmethod
    async def generate_one(cls, gender:str='any', safe:bool=True, locale:str='pt-BR'):
        try:
            fake = cls.get_instance(locale) 
            return await asyncio.to_thread(cls._generate_sync, fake, gender, safe)  
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @classmethod
    async def generate_many(cls, rows:int, gender:str='any', safe:bool=True, locale:str='pt-BR'): 
        try:
            gender = gender.lower()
            
            if rows <= 0:
                raise ValueError("'rows' parameter should not be less or equal than 0")

            fake = cls.get_instance(locale)

            def generate_users():
                return [cls._generate_sync(fake, gender, safe) for _ in range(rows)]

            data = await asyncio.to_thread(generate_users)
            return data
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))