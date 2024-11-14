# Flask-Template-Refs
A Flask extension allowing easy access to templates with dot notation and auto-completion.
## Overview
Keeping track of templates names when working on large Flask applications can be difficult, especially when working with libraries such as HTMX, which rely on rendering lots of template partials, often reused and shared across the whole application.

This can become especially problematic when refactoring, forcing us to track down every render_template() call to make sure the proper template name is used.

This extension aims to solve these issues and improve developer experience when working with templates.
## Features

### Access templates easily with dot notation
Templates are referenced with simple names in a dedicated class as instance attributes, so that you can use dot notation rather than strings and square brackets.

#### Before:
```python
from jinja_partials import render_partial

render_partial("shared/forms/inputs/file_input.jinja")
```
#### After:
```python
from flask_template_refs import refs
from jinja_partials import render_partial

render_partial(refs.file_input)
```
### Organize your template files however you like
Wether you create create sub directories or set blueprint specific folders, all templates listed in your app and its blueprints are mapped to a single object.

In case of templates sharing the same name, the name of their parent directory is appended at the start of its reference name.

#### Example:

`"button.jinja"`  and `"/templates/login/button.jinja"` are referenced under `refs.button` and `refs.login_button`.

### Benefit from auto-completion and linting
If a template's reference changes, you'll be able to catch it immediatly with the linter of your choice. You'll also benefit from suggestions and auto-completion, sparing you from having to remember every template's actual name.

![Auto-completion in Neovim](/assets/autocompletion-example.png)

## Quickstart
### Install the package

You can install the extension through your package manager of choice:
- Pip: `pip install flask-template-refs`
- Rye: `rye add flask-template-refs`
- Poetry: `poetry add flask-template-refs`

### Register the extension
Import the main extension class and pass the Flask `app` object to the constructor.

**Important:** blueprints should be registered **before** the extension, so that their template folders are mapped as well.

```python
from flask import Flask
from flask_template_refs import FlaskTemplateRefs

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
		
	#register all blueprints first
    app.register_blueprint(bp_1)
    app.register_blueprint(bp_2)

	#register the extension
    FlaskTemplateRefs(app)

    return app

```

### Import the `refs` module wherever you need to access templates
```python
from flask_template_refs import refs

@login.get('/')
def show():
    htmx = HTMX(current_app)
    form = LoginForm()

    try:
        if htmx:
        # access reference here
            return render_partial(
                refs.login_section, form=form), 200

		# and here
        return render_template(
            refs.base_layout, view=url_for('main.login.show'), form=form), 200

    except TemplateNotFound as e:
        abort(404)

```

### Access references in other templates through as Jinja globals
This template extends the template referenced under `refs.main`, and renders partial templates `refs.h2` and `refs.login_form`:

```jinja2 
{% extends MAIN %}
{% block main_content %}
    {{ render_partial(H2, text="Connexion") }}
    {% if error_message: %}<p>{{ error_message }}</p>{% endif %}
    {{ render_partial(LOGIN_FORM, form=form) }}
{% endblock %}
```
