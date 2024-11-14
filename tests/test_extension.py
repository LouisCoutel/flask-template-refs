import os

from pathlib import Path
from flask import render_template
from flask.testing import FlaskClient

from flask_template_refs.references import refs
from flask_template_refs.ftr import map_dir, resolve_tf


def test_map_empty_dir(root_path):
    result = map_dir(root_path / "empty")

    assert not result


def test_map_not_empty_dir(root_path):
    result = map_dir(root_path / "templates")

    assert result


def resolve_tf_str(root_path):
    assert resolve_tf(root_path, "templates") == root_path / "templates"


def resolve_tf_pathLike(root_path):
    assert resolve_tf(root_path, os.path.join(
        "templates", "level_2")) == Path(__file__).parent / "templates" / "level_2"


def resolve_tf_not_provided(root_path):
    assert resolve_tf(root_path, None) == root_path / "templates"




def test_refs_match_templates(root_path):
    refs = map_dir(root_path / "templates")
    expected_refs = ["test_1", "test_2", "level_2_test_1",
                     "level_3_test_2", "level_3_test_1"]

    assert refs
    assert all([ref == expected_refs[i] for i, ref in enumerate(refs)])


def test_globals_refs_set(app):

    expected_refs = ["test_1", "test_2", "level_2_test_1",
                     "level_3_test_2", "level_3_test_1"]

    for ref in expected_refs:
        assert app.jinja_env.globals.get(ref) is not None


def test_refs_file_written():
    assert all([refs.test_1, refs.test_2, refs.level_2_test_1,
               refs.level_3_test_2, refs.level_3_test_1])


def test_render_template(app):
    with app.app_context():
        result = render_template(refs.test_1)
        assert result == "<p>TEST</p>"


def test_with_blueprints_specific_folders(client: FlaskClient):
    res_bp_folder = client.get("/bp_1/")
    assert res_bp_folder.status_code == 200
    assert res_bp_folder.data == b"<p>TEST</p>"

    res_no_bp_folder = client.get("/bp_2/")
    assert res_no_bp_folder.status_code == 200
    assert res_no_bp_folder.data == b"<p>BP_TEST</p>"
