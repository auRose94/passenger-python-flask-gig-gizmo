import os

env = ""
if "FLASK_ENV" in os.environ:
    env = os.environ["FLASK_ENV"]
elif "PASSENGER_APP_ENV" in os.environ:
    env = os.environ["PASSENGER_APP_ENV"]
dev = env == "development" or env != "release"