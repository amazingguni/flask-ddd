
from app.order.domain.order import Order
from app.order.domain.shipping_info import ShippingInfo, Receiver, Address
from app.order.domain.order_state import OrderState


def test_select_by_orderer(pre_data_db_session, order_summary_dao):
    order_summaries = order_summary_dao.select_by_orderer(2)
    assert len(order_summaries) == 2
    summary = order_summaries[0]

    assert summary.order_id == 2
    assert summary.orderer_id == 2
    assert summary.orderer_username == '사용자1'
    assert summary.product_name == '라즈베리파이3 모델B'
    assert summary.total_amounts == 123920


def test_count_by_filter(pre_data_db_session, order_summary_dao):
    assert order_summary_dao.counts(None) == 4
    assert order_summary_dao.counts({'orderer_id': 2}) == 2
    assert order_summary_dao.counts({'orderer_id': 3}) == 1


def test_select_by_filter(pre_data_db_session, order_summary_dao):
    assert len(order_summary_dao.select(None, 0, 10)) == 4
    assert len(order_summary_dao.select({'orderer_id': 2}, 0, 10)) == 2
    assert len(order_summary_dao.select({'orderer_id': 3}, 0, 10)) == 1


def test_select_by_filter_limited_test(db_session, order_summary_dao, loginned_user):
    # Given
    shipping_info = ShippingInfo(
        receiver=Receiver('사용자1', '010-1234-5678'),
        address=Address('123456', '서울시', '관악구'),
        message='메시지')
    for _ in range(15):
        db_session.add(Order(
            orderer=loginned_user, shipping_info=shipping_info,
            state=OrderState.PREPARING
        ))
    db_session.commit()

    # When, Then
    filter = {
        'orderer_id': loginned_user.id
    }
    assert len(order_summary_dao.select(filter, 0, 10)) == 10
    assert len(order_summary_dao.select(filter, 0, 5)) == 5
    assert len(order_summary_dao.select(filter, 12, 5)) == 3
