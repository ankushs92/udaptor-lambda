import os


def get_env_variable(name):
    try:
        return os.environ.get(name)
    except KeyError:
        message = "Expected environment variable '{}' not set.".format(name)
        raise Exception(message)

def get_aws_keys():
    AWS_ACCESS_KEY = get_env_variable('aws_access_key_id')
    AWS_SECRET_KEY = get_env_variable('aws_secret_key')

    return AWS_ACCESS_KEY, AWS_SECRET_KEY

def create_db_url(user, pw, url, db):
    if user is None or pw is None:
        user, pw = ('', '')
    return "postgresql://{user}:{pw}@{url}/{db}".format(user=user, pw=pw, url=url, db=db)


def get_env_db_url(env_setting):
    if env_setting == "dev":
        POSTGRES_USER = get_env_variable("dev_postgres_user")
        POSTGRES_PW = get_env_variable("dev_postgres_pw")
        POSTGRES_URL = get_env_variable("dev_postgres_url")
        POSTGRES_DB = get_env_variable("dev_postgres_db")

    elif env_setting == "prod":
        POSTGRES_USER = get_env_variable("prod_postgres_user")
        POSTGRES_PW = get_env_variable("prod_postgres_pw")
        POSTGRES_URL = get_env_variable("prod_postgres_url")
        POSTGRES_DB = get_env_variable("prod_postgres_db")

    return create_db_url(POSTGRES_USER, POSTGRES_PW, POSTGRES_URL, POSTGRES_DB)


# DB URLS for each Environment
DEV_DB_URL = get_env_db_url("dev")
PROD_DB_URL = get_env_db_url("prod")


class Config(object):
    # SQLAlchemy settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = get_env_variable('SECRET_KEY')
    # Flask Settings
    DEBUG = False
    TESTING = False


class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = DEV_DB_URL
    FLASK_ENV = "development"
    DEBUG = True


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = PROD_DB_URL
    FLASK_ENV = "production"

    DEBUG = False
    TESTING = False
