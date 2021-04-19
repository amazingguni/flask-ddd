from app.user.domain.user import User

from app.order.domain.order import Order
from app.order.domain.shipping_info import ShippingInfo
from app.order.domain.order_state import OrderState
from app.order.domain.order_line import OrderLine


class PlaceOrderService:
    def __init__(self, cart_repository, order_repository):
        self.cart_repository = cart_repository
        self.order_repository = order_repository

    def place_order(self, orderer: User, shipping_info: ShippingInfo):
        order = Order(
            orderer=orderer,
            shipping_info=shipping_info,
            state=OrderState.PAYMENT_WAITING)
        carts = self.cart_repository.find_by_user(orderer)
        for cart in carts:
            order.order_lines.append(
                OrderLine(product=cart.product, quantity=cart.quantity))
        self.order_repository.save(order)
        return order
