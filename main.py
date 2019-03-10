# import os

from flask import Flask

from app.blueprint.authentication import authentication
from app.blueprint.user import user

print("name: ", __name__)
app = Flask(__name__)
app.register_blueprint(authentication)
app.register_blueprint(user)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
