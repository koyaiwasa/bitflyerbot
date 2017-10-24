from enum import Enum


class ChildOrder:

    def __init__(self,
                 product_code,
                 child_order_type,
                 side,
                 price: int,
                 size: float,
                 minute_to_expire: int,
                 time_in_force):
        self.product_code = product_code
        self.child_order_type = child_order_type
        self.side = side
        self.price = price
        self.size = size
        self.minute_to_expire = minute_to_expire
        self.time_in_force = time_in_force

    def to_body(self):
        return {
            "product_code": self.product_code.value,
            "child_order_type": self.child_order_type.value,
            "side": self.side.value,
            "price": self.price,
            "size": self.size,
            "minute_to_expire": self.minute_to_expire,
            "time_in_force": self.time_in_force.value
        }


class ProductCode(Enum):
    btc_jpy = "BTC_JPY"
    btc_fx = "FX_BTC_JPY"
    eth_btc = "ETH_BTC"


class ChildOrderType(Enum):
    limit = "LIMIT"  # 指値注文
    market = "MARKET"  # 成行注文


class Side(Enum):
    buy = "BUY"
    sell = "SELL"


class TimeInForce(Enum):
    good_till_canceled = "GTC"  # 注文が約定するかキャンセルされるまで有効
    immediate_or_cancel = "IOC"  # 指定した価格かそれよりも有利な価格で即時に一部あるいは全部を約定させ、約定しなかった注文数量をキャンセル
    fill_or_kill = "FOK"  # 発注の全数量が即座に約定しない場合当該注文をキャンセル
