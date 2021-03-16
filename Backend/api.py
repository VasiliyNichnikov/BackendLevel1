import flask

character_valid = "qwertyuiopasdfghjklzxcvbnm1234567890-."
blueprint = flask.Blueprint('api', __name__, template_folder="templates")