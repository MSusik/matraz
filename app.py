from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
db = SQLAlchemy(app)

@app.route('/')
def index():
    return "Hello world!"

if __name__ == '__main__':
    app.run()

