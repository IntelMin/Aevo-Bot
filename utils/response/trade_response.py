from time import ctime
from database.cache import get_trade_cache

def process_order_data(order):
    response = f"Order ID: {order['order_id']}\n"
    response += f"Asset Ticker: {order['instrument_name']}\n"
    response += f"Asset Type: {order['instrument_type']}\n"
    response += f"Order Type: {order['order_type']}\n"
    response += f"Trade Direction: {order['side']}\n"
    response += f"Quantity of Contracts: {int(order['amount']) / 10 ** 6}\n"
    response += f"Limit Price for Order: {order['price']}\n"
    response += f"Avg. Entry Price: {order['avg_price']}\n"
    response += f"Filled Amount: {order['filled']}\n"
    response += f"Order Status: {order['order_status']}\n"
    response += "---------------------------------------"

    return response

def respond_to_open_orders(data):
    if len(data) == 0:
        return "You have no Open orders at the moment..."
    response = ""
    for order in data:
        response += process_order_data(order)
        

    return response

def process_trade_cache(user_id):
    asset = get_trade_cache(user_id, 'asset')
    is_buy = get_trade_cache(user_id, 'is_buy')
    _trade_direction = 'buy' if is_buy else 'sell'
    request = get_trade_cache(user_id, 'request')
    quantity = get_trade_cache(user_id, 'quantity')
    limit_price = get_trade_cache(user_id, 'limit_price')
    order_type = "Market Order" if request == 'market_order' else "Limit Order"
    
    res_text =  f"Please confirm the order details below (Yes/No)\n\n"
    res_text += f"Asset: {asset}\n"
    res_text += f"Direction: {_trade_direction}\n"
    res_text += f"Quantity: {quantity} {asset} Contracts\n"
    res_text += f"Order Type: {order_type}\n"
    res_text += f"Limit Price: ${limit_price}\n" if request == 'limit_order' else ""
    
    return res_text

