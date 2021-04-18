
from app.order.domain.order import Order
from app.user.domain.user import User


class CancelPolicy:
    def has_cancellation_permission(self, order: Order,  canceller: User):
        if self.is_canceller_orderer(order, canceller):
            return True
        if canceller.is_admin:
            return True
        return False

    def is_canceller_orderer(self, order: Order,  canceller: User):
        return order.orderer == canceller
