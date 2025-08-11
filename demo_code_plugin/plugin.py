from flask import render_template, Blueprint, current_app
import os

source_code = Blueprint("About", __name__, template_folder=os.path.join(os.path.dirname(__file__), "templates"))

# # [main route] the route url can be anything, but "main" is needed as entry point
@source_code.route('/')
def main():
    base_exists = "base.html" in current_app.jinja_loader.list_templates()
    filepath = os.path.join(os.path.dirname(__file__), 'demo_code.py')
    with open(filepath, 'r', encoding='utf-8') as f:
        code = f.read()
    return render_template('example.html', base_exists=base_exists, code=code)


