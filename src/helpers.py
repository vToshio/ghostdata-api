from fastapi.exceptions import HTTPException
from faker import Faker

class Generator:
    '''
    Classe que armazena as instâncias de geradores Faker.
    '''
    _instances = {}

    @staticmethod 
    def get_instance(locale:str='pt-BR') -> Faker:
        '''
        Método estático que retorna um generator de acordo com a sua localidade.
        Caso o generator não exista, o próprio método faz a instanciação e o armazena no atributo _instances.
        '''
        if locale not in Generator._instances.values():
            Generator._instances[locale] = Faker(locale=locale)
        return Generator._instances[locale]

def generate_user(rows:int, locale:str='pt-BR'): 
    '''
    Função auxiliar que retorna um dicionário contendo os dados de um usuário.
    '''
    try:
        fake = Generator.get_instance(locale)

        data = {
            'status_code': 200,
            'users': [
                {
                    'id': i,
                    'first_name': fake.first_name(),
                    'last_name': fake.last_name(),
                    'email': fake.safe_email(),
                    'phone_number': fake.phone_number(),
                    'address': {
                        'number': fake.building_number(),
                        'street_name': fake.street_name(),
                        'city': fake.city(),
                        'country': fake.country(),
                        'postal_code': fake.postcode(),
                    }
                }
                for i in range(rows)
            ]
        }

        return data
    except HTTPException as err:
        return {'status_code': err.status_code, 'description': err.detail}
    except Exception as err:
        return {'status_code': 500, 'description': str(err)}