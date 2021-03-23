from flask import Blueprint, render_template

blueprint = Blueprint('catalog', __name__, url_prefix='/catalog')

@blueprint.route('/', methods=('GET',))
def index():
    return 'hello'
    # return render_template()
