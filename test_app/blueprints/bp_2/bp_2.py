from flask import Blueprint, abort, render_template, request


bp_2 = Blueprint("bp_2",
                 __name__,
                 url_prefix="/bp_2",
                 root_path="test_app/blueprints/bp_2",
                 template_folder="templates")


@bp_2.get("/")
def test_2():
    ref = request.form.get("ref")

    if ref is not None:
        return render_template(ref)
    abort(404)
