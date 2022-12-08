from .core import Cart, CartItem

def test_core_basic():
    c = Cart()
    assert c.total_price == 0
    assert c.uuid is not None

    c.add_item(CartItem("Produto 1", 5.0, 2))
    c.add_item(CartItem("Produto 2", 10.0, 1))
    assert c.total_price == 20.0
    assert c.is_valid
    assert not c.has_checkout_info

    c.personal_info = "Person Name"
    c.payment_info = "Credit Card Number"
    c.shipping_info = "Address"
    assert c.has_checkout_info
    assert c.transact_payment() == (True, None)
