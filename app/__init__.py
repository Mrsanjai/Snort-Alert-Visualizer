import os
from flask import Flask

def create_app():
    app = Flask(
        __name__,
        template_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'templates')),
        static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
    )

    # ✅ Required for flash() and session features
    app.secret_key = 'supersecretkey'  # Change this to a random, secure value for production

    # Register your blueprints
    from app.routes.views import views_bp
    app.register_blueprint(views_bp)

    return app
