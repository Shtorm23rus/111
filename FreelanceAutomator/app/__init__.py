from flask import Flask
from app.core.config import Config
from app.utils.logger import setup_logger
import os

def create_app():
    app = Flask(__name__, 
                template_folder='web/templates',
                static_folder='web/static')
    
    app.config.from_object(Config)
    
    setup_logger()
    
    from app.web.routes import main_bp
    app.register_blueprint(main_bp)
    
    return app
