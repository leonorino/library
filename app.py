from flask import Flask

app = Flask(__name__)
app['SECRET_KEY'] = "secret_key"


if __name__ == "__main__":
    app.run(host="localhost", port=8080)
