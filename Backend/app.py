from flask import Flask


app = Flask(__name__)
app.config['SECRET_KEY'] = 'v!hT49JOc,Nob_Hp5urgx.D8Adfy1zS6n?YBPCsM'


@app.route('/')
def main():
    return 'Server Operation (Done)'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
