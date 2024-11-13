from flask import render_template

from pathlib import Path

from flask.testing import FlaskClient

from templates_refs.errors import FolderNotFoundError, NoTemplatesError
from templates_refs.map_templates import map_templates
from templates_refs.references import refs

folders = Path(__file__).parent.parent / "test_templates_folders"


def test_map_no_tf(app_tf_not_set):
    refs = map_templates(app_tf_not_set)

    assert isinstance(refs, FolderNotFoundError)


def test_map_no_templates(app_tf_empty):
    refs = map_templates(app_tf_empty)

    assert isinstance(refs, NoTemplatesError)


def test_map_with_templates(app_tf_set):
    refs = map_templates(app_tf_set)

    assert not isinstance(refs, NoTemplatesError)


def test_refs_match_templates(app_tf_set):
    refs = map_templates(app_tf_set)
    expected_refs = ["test_1", "test_2", "level_2_test_1",
                     "level_3_test_2", "level_3_test_1"]

    assert not isinstance(refs, NoTemplatesError)
    assert not isinstance(refs, FolderNotFoundError)
    assert all([ref == expected_refs[i] for i, ref in enumerate(refs)])


def test_globals_refs_set(app_tf_set):
    assert app_tf_set.jinja_env.globals.get('template_refs') is not None


def test_refs_file_written():
    assert all([refs.test_1, refs.test_2, refs.level_2_test_1,
               refs.level_3_test_2, refs.level_3_test_1])


def test_render_template(app_tf_set):
    with app_tf_set.app_context():
        result = render_template(refs.test_1)
        assert result == "<p>TEST</p>"


def test_with_blueprints_specific_folders(client: FlaskClient):
    res_bp_folder = client.get("/bp_1/")
    assert res_bp_folder.status_code == 200
    assert res_bp_folder.data == b"<p>TEST</p>"

    res_no_bp_folder = client.get("/bp_2/")
    assert res_no_bp_folder.status_code == 200
    assert res_no_bp_folder.data == b"<p>BP_TEST</p>"
