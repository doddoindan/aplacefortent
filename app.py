
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
app = Flask(__name__)

@app.route('/')
def index():
    return "OK!!!"

if __name__ == "__main__":
    app.run()

