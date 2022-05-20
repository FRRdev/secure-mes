<h2 align="center">Secure Mes</h2>

### Project description:

Service for sending messages and encrypting them using neurocriptography algorithms. The service allows you to achieve a
more secure storage of messages in the database.

To encrypt the text, the Blowfish symmetric encryption algorithm is used.(Taken from the Crypto Library). The TPM(Tree
Parity Machine) model is used to generate the secret key.

### Tools

**Stack:**

- Python >= 3.8
- DRF >= 3.10
- Django ORM
- Postgres
- Celery
- Redis

## Start

#### 1) Create image

    docker-compose build

##### 2) Run container

    docker-compose up

##### 3) Go to address

    http://127.0.0.1:8000/api/v1/swagger/






