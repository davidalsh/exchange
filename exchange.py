from enum import Enum


class OrderType(Enum):
    buy = "Buy"
    sell = "Sell"


class OrderAction(Enum):
    add = "Add"
    remove = "Remove"


class Order:
    def __init__(
        self,
        order_id: int,
        order_type: OrderType,
        action: OrderAction,
        price: float,
        quantity: int,
    ):
        self.id = order_id
        self.type = order_type
        self.action = action
        self.price = price
        self.quantity = quantity


class Exchange:
    def __init__(self):
        self.buy_orders: list[Order] = []
        self.sell_orders: list[Order] = []

    def order_action(self, order: Order):
        orders = self.get_orders(order.type)
        for ex_order in orders:
            if order.price == ex_order.price and order.action == ex_order.action:
                if order.action == "Add":
                    ex_order.quantity += order.quantity
                else:
                    ex_order.quantity -= order.quantity
                return
        orders.append(order)

    def get_orders_with_best_price(self):
        buy_best_price = max(self.buy_orders, key=lambda el: el.price).price if self.buy_orders else None
        sell_best_price = min(self.sell_orders, key=lambda el: el.price).price if self.sell_orders else None
        return {
            "best_buy_price": buy_best_price,
            "best_sell_price": sell_best_price,
        }

    def get_orders(self, order_type: OrderType):
        return self.buy_orders if order_type == "Buy" else self.sell_orders

    def clear_orders(self):
        self.buy_orders = list(filter(lambda order: order.quantity > 0, self.buy_orders))
        self.sell_orders = list(filter(lambda order: order.quantity > 0, self.sell_orders))

    def process_order(self, order: Order):
        self.order_action(order)
        self.clear_orders()
        print(self.get_orders_with_best_price())


new_orders = [
    {"order_id": 1, "order_type": "Buy", "action": "Add", "price": 20.00, "quantity": 100},
    {"order_id": 2, "order_type": "Sell", "action": "Add", "price": 25.00, "quantity": 200},
    {"order_id": 3, "order_type": "Buy", "action": "Add", "price": 23.00, "quantity": 50},
    {"order_id": 4, "order_type": "Buy", "action": "Add", "price": 23.00, "quantity": 70},
    {"order_id": 3, "order_type": "Buy", "action": "Remove", "price": 23.00, "quantity": 50},
    {"order_id": 5, "order_type": "Sell", "action": "Add", "price": 28.00, "quantity": 100},
]

exchange = Exchange()

for new_order in new_orders:
    exchange.process_order(
        Order(**new_order),
    )

