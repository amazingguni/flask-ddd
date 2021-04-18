from app.user.domain.user import User
from app.order.domain.order_repository import OrderRepository
from app.order.domain.cancel_policy import CancelPolicy
from .exceptions import NoOrderException, NoCancellablePermission


class CancelOrderService:
    def __init__(self, order_repository: OrderRepository):
        self.order_repository = order_repository
        self.cancel_policy = CancelPolicy()

    def cancel(self, order_id: int, canceller: User):
        order = self.find_order(order_id)
        if not self.cancel_policy.has_cancellation_permission(order, canceller):
            raise NoCancellablePermission
        order.cancel()
        self.order_repository.save(order)

    def find_order(self, order_id: int):
        order = self.order_repository.find_by_id(order_id)
        if not order:
            raise NoOrderException
        return order
