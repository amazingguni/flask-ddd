from flask import Blueprint, render_template

bp = Blueprint('catalog', __name__, 
    template_folder='../templates', static_folder="../static", url_prefix='/catalog/')

@bp.route('/categories', methods=('GET',))
def categories():
    return render_template('catalog/categories.html')
