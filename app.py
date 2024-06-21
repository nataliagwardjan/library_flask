from flask import Flask

app = Flask(__name__)
app.config['DEBUG'] = True

from main.controller import controller

if __name__ == "__main__":
    app.run(debug=True)
