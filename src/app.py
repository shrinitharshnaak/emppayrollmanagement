from flask import Flask, render_template
from .config import Config
from .database import db, init_app

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize database with models and seeder
    init_app(app)
    
    # Import and register blueprints
    from .routes import init_routes
    init_routes(app)
    
    @app.route('/')
    def home():
        return render_template('home.html')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)