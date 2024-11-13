import flask
import pytest
from flask.app import Flask
from pathlib import Path

from templates_refs.jinja_templates_refs import JinjaTemplatesRefs
from templates_refs.references import refs

template_folder = Path(
    __file__).parent / "templates"
empty_folder = Path(
    __file__).parent / "empty"
bp_folder = Path(
    __file__).parent / "bp_templates"


@pytest.fixture
def app_tf_not_set():
    app = flask.Flask("test_app")

    JinjaTemplatesRefs(app)

    yield app


@pytest.fixture
def app_tf_empty():
    app = flask.Flask("test_app", template_folder=empty_folder)

    JinjaTemplatesRefs(app)

    yield app


@pytest.fixture
def app_tf_set():
    app = flask.Flask("test_app", template_folder=template_folder)

    JinjaTemplatesRefs(app)

    yield app


@pytest.fixture
def app_with_bp():
    app = flask.Flask("test_app", template_folder=template_folder)

    bp_1 = flask.Blueprint("bp_1", "bp_1", url_prefix="/bp_1")
    bp_2 = flask.Blueprint(
        "bp_2", "bp_2", url_prefix="/bp_2", template_folder=bp_folder)

    @bp_1.get("/")
    def test_1():
        return flask.render_template(refs.test_1)

    @bp_2.get("/")
    def test_2():
        return flask.render_template(refs.bp_test)

    app.register_blueprint(bp_1)
    app.register_blueprint(bp_2)

    JinjaTemplatesRefs(app)

    yield app


@pytest.fixture
def client(app_with_bp: Flask):
    yield app_with_bp.test_client()
