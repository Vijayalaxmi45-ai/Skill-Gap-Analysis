from flask import Flask
from utils import db


def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    # NOTE: replace with a secure secret in production or read from env
    app.secret_key = 'dev-secret-key'

    # Register blueprints from the routes package
    from routes.main import main as main_bp
    from routes.auth import auth as auth_bp
    from routes.upload_resume import upload as upload_bp
    from routes.dashboard import dashboard as dashboard_bp
    from routes.company import company_bp
    from routes.analysis import analysis as analysis_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(company_bp)
    app.register_blueprint(analysis_bp)

    # Ensure DB connections are closed after each request
    app.teardown_appcontext(db.close_connection)

    return app


if __name__ == '__main__':
    application = create_app()
    # Run development server
    application.run(host='127.0.0.1', port=5000, debug=True)
