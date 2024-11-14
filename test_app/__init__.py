from flask import Flask, Blueprint, render_template
from flask_template_refs import FlaskTemplateRefs, refs


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(EXPLAIN_TEMPLATE_LOADING=True)

    bp_1 = Blueprint("bp_1", "bp_1", url_prefix="/bp_1")
    bp_2 = Blueprint(
        "bp_2", "bp_2", url_prefix="/bp_2", root_path="test_app", template_folder="bp_templates")

    @bp_1.get("/")
    def test_1():
        return render_template(refs.test_1)

    @bp_2.get("/")
    def test_2():
        return render_template(refs.bp_test)

    app.register_blueprint(bp_1)
    app.register_blueprint(bp_2)

    FlaskTemplateRefs(app)
    return app
