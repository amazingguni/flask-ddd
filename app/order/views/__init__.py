from flask import Blueprint, render_template, redirect, url_for
from dependency_injector.wiring import inject, Provide

from app.containers import Container
bp = Blueprint('order', __name__,
               template_folder='../templates', static_folder="../static", url_prefix='/order/')


@bp.route('/add', methods=['POST', ])
def add():
    return redirect(url_for('order.confirm'))


@bp.route('/confirm', methods=['GET', ])
def confirm():
    pass
