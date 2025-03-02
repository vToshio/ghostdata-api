from fastapi.exceptions import HTTPException
from faker import Faker

class Generator:
    '''
    Classe que armazena as instâncias de geradores Faker e métodos de requisição de dados.
    '''
    _instances = {}

    def _generate_email(first:str, last:str, safe:bool, fake:Faker):
        '''
        Gera um e-mail seguro (ou não) de acordo com o primeiro e último nome de uma pessoa
        '''
        return f'{first.lower().replace(' ', '')}.{last.lower().replace(' ', '')}@{fake.safe_domain_name() if safe else fake.domain_name()}'

    @staticmethod 
    def get_instance(locale:str='pt-BR') -> Faker:
        '''
        Método estático que retorna um generator de acordo com a sua localidade.
        Caso o generator não exista, o próprio método faz a instanciação e o armazena no atributo _instances.
        '''
        if locale not in Generator._instances:
            Generator._instances[locale] = Faker(locale=locale)
        return Generator._instances[locale]

    @staticmethod
    def generate_user(gender:str='any', safe:bool=True, locale:str='pt-BR'):
        '''
        Método estático que gera os dados de um único usuário, de acordo com o sexo.

        Args:
        - gender(str): define o sexo do usuário criado, sendo 'f', 'm', ou 'any'.
        - safe(bool): se o e-mail gerado é um e-mail não oficial ou não.
        - locale(str): define a localização de origem dos dados ('pt-BR', 'en-US', etc...)
        '''
        try:
            if gender not in ['f', 'm', 'any']:
                raise KeyError("'gender' parameter should be 'm', 'f' or 'any'")

            fake = Generator.get_instance(locale)
            
            genders = {
                'f': fake.first_name_female(),
                'm': fake.first_name_male(),
                'any': fake.first_name(),
            }

            first = genders[gender]
            last = fake.last_name()
            email = Generator._generate_email(first, last, safe, fake)

            data = {
                'id': fake.random_int(),
                'first_name': first,
                'last_name': last,
                'email': email,
                'phone_number': fake.phone_number(),
                'address': {
                    'number': fake.building_number(),
                    'street_name': fake.street_name(),
                    'city': fake.city(),
                    'country': fake.country(),
                    'postal_code': fake.postcode(),
                }
            }

            return data
        except KeyError as err:
            raise HTTPException(status_code=400, detail=str(err))
        except Exception as err:
            raise HTTPException(status_code=500, detail=str(err))

    @staticmethod
    def generate_users(rows:int, gender:str='any', safe:bool=True, locale:str='pt-BR'): 
        '''
        Método estático que gera os dados de n de usuários, de acordo com o valor definido em 'rows'.

        Args:
        - rows(int): define a quantidade de registros falsos de usuários
        - gender(str): define o sexo do usuário criado, sendo 'f', 'm', ou 'any'.
        - safe(bool): se o e-mail gerado é um e-mail não oficial ou não.
        - locale(str): define a localização de origem dos dados ('pt-BR', 'en-US', etc...)
        '''
        try:
            if rows <= 0:
                raise ValueError("'rows' parameter should not be less or equal than 0")
            if gender.lower() not in ['f', 'm', 'any']:
                raise KeyError("'gender' paremeter should be 'f', 'm' or 'any'")
            
            fake = Generator.get_instance(locale)

            genders = {
                'f': fake.first_name_female,
                'm': fake.first_name_male,
                'any': fake.first_name
            }

            data = dict()
            for i in range(rows):
                first = genders[gender]()
                last = fake.last_name()
                email = Generator._generate_email(first, last, safe, fake)

                data[i] = {
                    'id': fake.random_int(),
                    'first_name': first,
                    'last_name': last,
                    'email': email,
                    'phone_number': fake.phone_number(),
                    'address': {
                        'number': fake.building_number(),
                        'street_name': fake.street_name(),
                        'city': fake.city(),
                        'country': fake.country(),
                        'postal_code': fake.postcode(),
                    }
                }

            return data
        except ValueError as err:
            raise HTTPException(status_code=400, detail=str(err))
        except KeyError as err:
            raise HTTPException(status_code=400, detail=str(err))
        except Exception as err:
                raise HTTPException(status_code=500, detail=str(err))