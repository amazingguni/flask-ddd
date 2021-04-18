import pytest
from flask import url_for

from app.user.domain.user import User
from app.catalog.domain.product import Product
from app.order.domain.order import Order
from app.order.domain.order_line import OrderLine
from app.order.domain.shipping_info import ShippingInfo
from app.order.domain.order_state import OrderState

from app.tests import utils


def test_confirm(db_session, client, captured_templates, loginned_user):
    # Given
    product = Product(
        name='라즈베리파이3 모델B', price=56000, detail='모델B')
    db_session.add(product)
    db_session.commit()

    # When
    response = client.get(
        url_for('order.confirm', quantity=1, product_id=product.id))

    # Then
    assert response.status_code == 200
    template, context = captured_templates[0]
    assert template.name == 'order/order_confirm.html.j2'
    assert context['orderer'] == loginned_user
    assert len(context['order_products']) == 1
    assert context['order_products'][0].product_id == product.id


def test_confirm_invalid_product_id(db_session, client):
    response = client.get(
        url_for('order.confirm', quantity=1, product_id='invalid'))
    assert response.status_code == 500


def test_place(db_session, client, loginned_user):
    # Given
    product = Product(
        name='라즈베리파이3 모델B', price=56000, detail='모델B')
    db_session.add(product)
    db_session.commit()

    # When
    response = client.post(url_for('order.place'), data={
        'shipping_info.receiver.name': 'Guni',
        'shipping_info.receiver.phone': '010-0000-0000',
        'shipping_info.address.zip_code': '00000',
        'shipping_info.address.address1': '관악구',
        'shipping_info.address.address2': '대한민국 서울',
        'shipping_info.message': '빨리 가져다 주셔요',
        'order_products[0].product_id': str(product.id),
        'order_products[0].quantity': 1,
    })

    # Then
    assert response.status_code == 302
    order = db_session.query(Order).first()
    assert order.orderer == loginned_user
    assert order.shipping_info.receiver.name == 'Guni'
    assert order.shipping_info.receiver.phone == '010-0000-0000'
    assert order.shipping_info.address.zip_code == '00000'
    assert order.shipping_info.address.address1 == '관악구'
    assert order.shipping_info.address.address2 == '대한민국 서울'
    assert order.shipping_info.message == '빨리 가져다 주셔요'
    assert order.get_total_amounts() == 56000
    assert order.state == OrderState.PAYMENT_WAITING


def test_cancel(db_session, client, loginned_user, order):
    # When
    response = client.post(url_for('order.cancel', order_id=order.id))

    # Then
    utils.assert_redirect_response(
        response, url_for('order.canceled', order_id=order.id))
    db_session.refresh(order)
    assert order.state == OrderState.CANCELED


def test_change_shipping_info_page(client, captured_templates, order):
    # When
    response = client.get(
        url_for('order.change_shipping_info', order_id=order.id))

    # Then
    assert response.status_code == 200
    template, context = captured_templates[0]
    assert template.name == 'order/change_shipping_info.html.j2'
    assert context['order'] == order


def test_change_shipping_info_submit(db_session, client, order):
    # When
    response = client.post(
        url_for('order.change_shipping_info', order_id=order.id),
        data={
            'shipping_info.receiver.name': 'Changed',
            'shipping_info.receiver.phone': 'xxx-xxx-xxxx',
            'shipping_info.address.zip_code': '11111',
            'shipping_info.address.address1': '금천구구',
            'shipping_info.address.address2': '미국',
            'shipping_info.message': 'hurry up', })

    # Then
    utils.assert_redirect_response(response, url_for(
        'user.order_detail', order_id=order.id))
    db_session.refresh(order)
    assert order.shipping_info.receiver.name == 'Changed'
