import os
basedir = os.path.abspath(os.path.dirname(__file__))

## DATABASE CONFIG#######################################
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
if os.environ.get('DATABASE_URL') is None:  ## LOCAL
    SQLALCHEMY_DATABASE_URI = 'postgres://postgres:1@localhost/postgres';# 'sqlite:///' + os.path.join(basedir, 'app.db')
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
else:  #PRODUCTION
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    OAUTH_CREDENTIALS = {
    'facebook': {
            'id': '1012327082122718',
        'secret': 'ec32784af5a77d1ddfd050f351e39dc4'

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

PROPAGATE_EXCEPTIONS = True


