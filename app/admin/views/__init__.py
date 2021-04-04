from flask import Blueprint, render_template
# from app.order.query.application.order_view_list_service import get_list
bp = Blueprint('admin', __name__, 
    template_folder='../templates', static_folder="../static", url_prefix='/admin/')

@bp.route('/', methods=('GET',))
def index():
    return render_template('admin/index.html')

@bp.route('/orders', methods=('GET',))
def orders():
    # summaries = get_list()
    return render_template('admin/orders.html')