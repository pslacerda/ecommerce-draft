from flask import Flask, request, jsonify
from typing import Dict

from .core import Cart, CartItem


app = Flask(__name__)
carts: Dict[str, Cart] = {}


def resp(status, obj):
    return jsonify({
        "status": status,
        "response": obj
    })


@app.route("/new_cart", methods=["POST"])
def new_cart():
    cart = Cart()
    carts[cart.uuid] = cart
    return resp("OK", cart)


@app.route("/show_cart/<cart_uuid>", methods=['GET'])
def show_carts(cart_uuid):
    return resp("OK", carts[cart_uuid])


@app.route("/add_item/<cart_uuid>", methods=["POST"])
def add_item(cart_uuid):
    req = request.get_json()
    item = CartItem(req['title'], req['price'], req['quantity'])
    
    carts[cart_uuid].add_item(item)
    return resp("OK", item)


@app.route("/del_item/<cart_uuid>/<item_uuid>", methods=["DELETE"])
def del_item(cart_uuid, item_uuid):
    del carts[cart_uuid].items[item_uuid]
    return resp("OK", None)


@app.route("/checkout/<cart_uuid>", methods=["POST"])
def checkout(cart_uuid):
    cart = carts[cart_uuid]
    req = request.get_json()

    cart.personal_info = req['personal_info']
    cart.payment_info = req['payment_info']
    cart.shipping_info = req['shipping_info']

    assert cart.has_checkout_info
    cart.transact_payment()
    return resp("OK", None)
