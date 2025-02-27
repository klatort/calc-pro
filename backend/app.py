from flask import Flask
from flask_cors import CORS
from config import Config
from routes.get_calc_plus import route_calc
from routes.get_flavors import route_flavors
from routes.get_test import route_test
import os
from asgiref.wsgi import WsgiToAsgi


def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config.from_object(Config)

    app.register_blueprint(route_calc, url_prefix='/calc')
    app.register_blueprint(route_flavors, url_prefix='/flavor')
    app.register_blueprint(route_test, url_prefix='/test')
    
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    return app


app = create_app()
asgi_app = WsgiToAsgi(app)

if __name__ == '__main__':
    app.run(debug=True)
