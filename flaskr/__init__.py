from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__,instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        UPLOAD_FOLDER='downloads/')
    
    @app.route('/inicial')
    def teste():
        return 'tela teste'
    import homepage
    app.register_blueprint(homepage.bp)
    app.add_url_rule('/',endpoint='index')
    return app
