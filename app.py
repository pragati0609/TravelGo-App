import os
from flask import Flask, render_template
from config import config_by_name
from routes.auth import auth_bp
from routes.booking import booking_bp
from routes.dashboard import dashboard_bp
from services.aws_service import aws_service

def create_app(config_name=None):
    """Application factory for TravelGo."""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')

    app = Flask(__name__)
    app.config.from_object(config_by_name.get(config_name, config_by_name['default']))

    # Initialize DynamoDB tables if live AWS connection is available
    with app.app_context():
        try:
            aws_service.create_tables_if_not_exist()
        except Exception as e:
            app.logger.warning(f"DynamoDB initialization warning: {e}")

    # Register Blueprints
    app.register_blueprint(booking_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp)

    # Context processor for global template variables
    @app.context_processor
    def inject_global_data():
        return {
            'aws_region': app.config.get('AWS_REGION', 'ap-south-1'),
            'app_version': '1.0.0'
        }

    # Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    return app

app = create_app()

if __name__ == '__main__':
    # Default Flask port 5000 as specified in course EC2 security group requirements
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
