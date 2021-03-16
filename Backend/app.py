from flask import Flask
from api import blueprint
from DataBase import db_session


app = Flask(__name__)
app.config['SECRET_KEY'] = 'v!hT49JOc,Nob_Hp5urgx.D8Adfy1zS6n?YBPCsM'
app.register_blueprint(blueprint)


@app.route('/')
def main():
    return 'Server Operation (Done)'


if __name__ == '__main__':
    db_session.global_init('DataBase/data_base.db')
    app.run(host='0.0.0.0', port=8000)
