from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Dict, Optional, Tuple
from uuid import uuid4

MAX_CART_ENTRIES = 1000
CART_VALIDATE = timedelta(minutes=100)


class MaxCartEntriesReached(Exception):
    pass


class ExpiredCart(Exception):
    pass


class IncompleteInfo(Exception):
    pass


@dataclass
class UuidMixin:
    uuid: str = field(init=False)

    def __post_init__(self):
        self.uuid = str(uuid4())


@dataclass
class CartItem(UuidMixin):
    title: str
    price: float
    quantity: int


@dataclass
class Cart(UuidMixin):

    items: Dict[str, CartItem] = field(default_factory=dict)
    last_added: datetime = field(default_factory=datetime.now)

    personal_info: Optional[str] = None
    payment_info: Optional[str] = None
    shipping_info: Optional[str] = None

    @property
    def total_price(self):
        return sum(i.price * i.quantity for i in self.items.values())

    @property
    def is_valid(self):
        return datetime.now() - self.last_added <= CART_VALIDATE

    @property
    def has_checkout_info(self):
        return (
            self.personal_info is not None
            and self.payment_info is not None
            and self.shipping_info is not None
        )

    def add_item(self, item: CartItem) -> None:
        if len(self.items) > MAX_CART_ENTRIES:
            raise MaxCartEntriesReached
        if not self.is_valid:
            raise ExpiredCart
        self.last_added = datetime.now()
        self.items[item.uuid] = item
        return item.uuid

    def del_item(self, item_uuid: str) -> None:
        del self.items[item_uuid]

    def transact_payment(self) -> Tuple[bool, Optional[str]]:
        if not self.has_checkout_info or len(self.items) == 0:
            raise IncompleteInfo
        if not self.is_valid:
            raise ExpiredCart
        try:
            pass  # TODO
        except Exception as exc:  # pylint: disable=broad-except
            return False, str(exc)
        return True, None
