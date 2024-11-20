from flask import Flask
from flask_template_refs.ftr import FlaskTemplateRefs
from test_app.blueprints.bp_1 import bp_1
from test_app.blueprints.bp_2.bp_2 import bp_2


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(EXPLAIN_TEMPLATE_LOADING=True)

    app.register_blueprint(bp_1)
    app.register_blueprint(bp_2)

    FlaskTemplateRefs(app)

    return app
