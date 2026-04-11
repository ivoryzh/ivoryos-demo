from flask import Blueprint, render_template, current_app
import os

docs_bp = Blueprint("readme", __name__,
                    template_folder=os.path.join(os.path.dirname(__file__), "templates"), 
                    static_folder="../docs")

@docs_bp.route('/')
def main():
    # Detect if we are running inside IvoryOS environment where base.html exists
    base_exists = False
    if current_app and hasattr(current_app, 'jinja_loader') and current_app.jinja_loader:
        try:
            base_exists = "base.html" in current_app.jinja_loader.list_templates()
        except:
            pass
            
    return render_template('docs.html', base_exists=base_exists)
