

from flask import url_for

from app.user.domain.user import User
from app.catalog.domain.product import Product

from app.tests import utils


def test_add_order(db_session, client, captured_templates):
    user = User(username='사용자1', password='1234',
                blocked=False, is_admin=False)
    product = Product(
        name='라즈베리파이3 모델B', price=56000, detail='모델B')

    db_session.add_all([user, product])
    response = client.post(url_for('order.add'), data={
        'product_id': product.id,
        'quantity': 1
    })

    utils.assert_redirect_response(response, url_for('order.confirm'))
