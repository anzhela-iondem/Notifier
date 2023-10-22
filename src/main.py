from flask import Flask

from src.app.views import APIView


def main():
    app = Flask(__name__)
    app.add_url_rule("/", view_func=APIView.as_view("/"))
    app.run()


if __name__ == "__main__":
    main()
