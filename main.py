from flask import Flask
from flask_session import Session
from app import default_blueprint

sess = Session()

app = Flask(__name__)

app.register_blueprint(default_blueprint)

if __name__ == "__main__":
    
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    
    sess.init_app(app)

    app.debug = True
    app.run(host='0.0.0.0', port=5000)