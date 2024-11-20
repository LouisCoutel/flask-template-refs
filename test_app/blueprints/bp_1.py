import logging
from flask import Blueprint, abort, render_template, request


bp_1 = Blueprint("bp_1", __name__, url_prefix="/bp_1")


@bp_1.get("/")
def test_1():
    ref = request.form.get("ref")

    if ref is not None:
        return render_template(ref)

    abort(404)
