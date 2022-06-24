import falcon
import psycopg2
import logging
import email_validator


class Users:
    def __init__(self, db):
        self.cur = db.cur
    
    async def on_post(self, req, resp):
        data = await req.get_media()

        self.validate_data(data)
        self.insert_data(data)

        resp.media = {}
        resp.status = falcon.HTTP_200

    def validate_data(self, data):
        if not isinstance(data, dict):
            raise falcon.HTTPBadRequest(description='Kod błędu 0x003, skontaktuj się z administratorem')

        mandatory_params = ['email', 'first_name', 'last_name', 'job_id', 'education_id']
        optional_params = ['phone', 'address']

        # sprawdzenie parametrów obowiązkowych
        for param in mandatory_params:
            if param not in data:
                logging.info(data)
                logging.error("Missing param: {}".format(param))
                raise falcon.HTTPBadRequest(description='Kod błędu 0x003, skontaktuj się z administratorem')

            data[param] = data[param].strip()

        # uzupełnienie brakujących parametrów opcjonalnych 
        for param in optional_params:
            if param not in data:
                data[param] = ''

        try:
            email_validator.validate_email(data['email'])
        except email_validator.EmailNotValidError:
            raise falcon.HTTPBadRequest(description='Niepoprawny adres email', code='email')

        if data['first_name'] == '':
            raise falcon.HTTPBadRequest(description='Pole nie może być puste', code='first_name')
            
        if data['last_name'] == '':
            raise falcon.HTTPBadRequest(description='Pole nie może być puste', code='last_name')

    def insert_data(self, data):
        q = '''
            INSERT INTO users (email, first_name, last_name, phone, address, job_id, education_id)
            VALUES (%(email)s, %(first_name)s, %(last_name)s, %(phone)s, %(address)s, %(job_id)s, %(education_id)s)
        '''

        try:
            self.cur.execute(q, data)
        except psycopg2.errors.UniqueViolation:
            raise falcon.HTTPBadRequest(description='Podany email już istnieje', code='email')
        except psycopg2.errors.ForeignKeyViolation as e:
            logging.info(data)
            logging.error(e)
            raise falcon.HTTPBadRequest(description='Kod błędu 0x001, skontaktuj się z administratorem')
        except Exception as e:
            logging.info(data)
            logging.error(e)
            raise falcon.HTTPBadRequest(description='Kod błędu 0x002, skontaktuj się z administratorem')

