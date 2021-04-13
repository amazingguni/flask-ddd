from .order_request import OrderRequest
from ..domain.order import Order
from ..domain.order_state import OrderState
from ..domain.order_line import OrderLine


class PlaceOrderService:
    def __init__(self, product_repository, order_repository):
        self.product_repository = product_repository
        self.order_repository = order_repository

    def place_order(self, order_request: OrderRequest):

        order_lines = []
        for op in order_request.order_products:
            product = self.product_repository.find_by_id(op.product_id)
            order_lines.append(
                OrderLine(product=product, quantity=op.quantity))
        print('!!!', self.order_repository.session)
        print('!!!', self.product_repository.session)
        order = Order(
            orderer=order_request.orderer,
            order_lines=order_lines,
            shipping_info=order_request.shipping_info,
            state=OrderState.PAYMENT_WAITING)

        self.order_repository.save(order)
        return order
