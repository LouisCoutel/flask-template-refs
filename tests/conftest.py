import flask
import pytest

from pathlib import Path
from flask.app import Flask

from flask_template_refs.references import refs
from flask_template_refs.ftr import FlaskTemplateRefs


@pytest.fixture
def root_path():
    yield Path(__file__).parent.parent


@pytest.fixture
def app():
    app = flask.Flask("test_app")

    bp_1 = flask.Blueprint("bp_1", "bp_1", url_prefix="/bp_1")
    bp_2 = flask.Blueprint(
        "bp_2", "bp_2", url_prefix="/bp_2", template_folder="bp_templates")

    @bp_1.get("/")
    def test_1():
        return flask.render_template(refs.test_1)

    @bp_2.get("/")
    def test_2():
        return flask.render_template(refs.bp_test)

    app.register_blueprint(bp_1)
    app.register_blueprint(bp_2)

    FlaskTemplateRefs(app)

    yield app


@pytest.fixture
def client(app: Flask):
    yield app.test_client()
