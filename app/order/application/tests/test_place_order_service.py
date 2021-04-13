
import pytest
from ..place_order_service import PlaceOrderService
from ..order_product import OrderProduct
from ..order_request import OrderRequest
from ...domain.shipping_info import ShippingInfo
from ...domain.order import Order
from ...domain.order_state import OrderState
from app.catalog.domain.product import Product
from app.user.domain.user import User


@pytest.fixture(scope='function')
def place_order_service(product_repository, order_repository):
    return PlaceOrderService(
        product_repository=product_repository, order_repository=order_repository)


# def test_place_order(pre_data_db_session, place_order_service, shipping_info):
#     # Given
#     product = pre_data_db_session.query(Product).first()
#     orderer = pre_data_db_session.query(User).first()
#     order_product = OrderProduct(product_id=product.id, quantity=1)
#     request = OrderRequest(order_products=[order_product],
#                            orderer=orderer, shipping_info=shipping_info)

#     # When
#     order = place_order_service.place_order(request)

#     # Then
#     # order = pre_data_db_session.query(Order).first()
#     assert order.orderer == orderer
#     assert order.shipping_info.receiver.phone == shipping_info.receiver.phone
#     assert order.shipping_info.receiver.name == shipping_info.receiver.name
#     assert order.state == OrderState.PAYMENT_WAITING
#     assert len(order.order_lines) == 1
