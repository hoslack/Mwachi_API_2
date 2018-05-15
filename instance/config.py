import os


class Config(object):
    """This is the main configuration class"""
    DEBUG = False
    SECRET = os.environ.get('SECRET')
    CSRF_ENABLED = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')


class DevelopmentConfig(Config):
    """This is the development configuration class"""
    DEBUG = True


class ProductionConfig(Config):
    """This is the production configuration class"""
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig
}
