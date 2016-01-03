import os
basedir = os.path.abspath(os.path.dirname(__file__))

## DATABASE CONFIG#######################################
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
if os.environ.get('DATABASE_URL') is None:  ## PRODUCTION
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
    OAUTH_CREDENTIALS = {
    'facebook': {
        'id': '10123270dfndm82122718',
        'secret': '29351829c68ccb624e6bc916bee7567d'
    },
    'twitter': {
        'id': '3RzWQclolxWZIMq5LJqzRZPTl',
        'secret': 'm9TEd58DSEtRrZHpz2EjrV9AhsBRxKMo8m3kuIZj3zLwzwIimt'
    }
}    
else:  #LOCAL
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    OAUTH_CREDENTIALS = {
    'facebook': {
        'id': '416771981865519',
        'secret': 'cda72d0115429b3827bd626aa80c9bd5'
    },
    'twitter': {
        'id': '3RzWQclolxWZIMq5LJqzRZPTl',
        'secret': 'm9TEd58DSEtRrZHpz2EjrV9AhsBRxKMo8m3kuIZj3zLwzwIimt'
    }
}    

SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    
## FORMS CSRF####################    
WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'


## AUTORIZATION##############################
OUTHID_PROVIDERS = ['facebook']


