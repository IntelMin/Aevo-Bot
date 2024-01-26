from time import ctime

def respond_to_trade_history(response_body):
    response = ""
    count = response_body.get('count', '0')
    response += f"Total Number of Trades: {count}\n\n"

    trade_history = response_body.get('trade_history', [])
    if len(trade_history) == 0:
        return "You have no trade history between the specified time period"
    for trade in trade_history:
        response += f"Trade ID: {trade.get('trade_id', 'N/A')}\n"
        response += f"Order ID: {trade.get('order_id', 'N/A')}\n"
        response += f"Trade Type: {trade.get('trade_type', 'N/A')}\n"
        response += f"Asset: {trade.get('asset', 'ETH')}\n"
        response += f"Asset Ticker: {trade['instrument_name']}\n"
        response += f"Asset Type: {trade['instrument_type']}\n"
        response += f"Spot Price: ${trade.get('spot_price', '0')}\n"
        response += f"Quantity of Contracts: {int(trade['amount']) / 10 ** 6}\n"
        response += f"Limit Price of Order: ${trade.get('price', '0')}\n"
        response += f"Avg. Price: ${trade.get('avg_price', '0')}\n"
        response += f"Trade Direction: {trade.get('side', 'N/A')}\n"
        response += f"Fees Paid: {trade.get('fees', '0')}\n"
        response += f"Profit and Loss: {trade.get('pnl', '0')}\n"
        response += f"Trade Status: {trade.get('trade_status', 'N/A')}\n"
        response += f"Liquidation Fee: {trade.get('liquidation_fee', 'N/A')}\n"
        response += f"Created Timestamp: {ctime(int(trade.get('created_timestamp', 'N/A')) / 10**9)}\n\n"

    return response

def respond_to_order_history(response_body):
    response = ""
    count = response_body.get('count', '0')
    response += f"Total Number of Orders: {count}\n\n"

    order_history = response_body.get('order_history', [])
    if len(order_history) == 0:
        return "You have no order history between the specified time period"
    for order in order_history:
        response += f"Order ID: {order.get('order_id', 'N/A')}\n"
        response += f"Order Type: {order.get('order_type', 'N/A')}\n"
        response += f"Asset Ticker: {order.get('instrument_name', 'N/A')}\n"
        response += f"Asset Type: {order.get('instrument_type', 'N/A')}\n"
        response += f"Trade Direction: {order.get('side', 'N/A')}\n"
        response += f"Quantity of Contracts: {int(order['amount']) / 10 ** 6}\n"
        response += f"Price: ${order.get('price', '0')}\n"
        response += f"Amount Filled: {order.get('filled', 'N/A')}\n"
        response += f"Error: {order.get('error', 'N/A')}\n"
        response += f"Order Status: {order.get('order_status', 'N/A')}\n"
        response += f"Created Timestamp: {ctime(int(order.get('created_timestamp', 'N/A')) / 10**9)}\n\n"

    return response

def respond_to_portfolio_request(response_body):
    response = "Your Account Portfolio Data\n\n"
    balance = response_body.get('balance', 'N/A')
    pnl = response_body.get('pnl', 'N/A')
    realized_pnl = response_body.get('realized_pnl', 'N/A')
    profit_factor = response_body.get('profit_factor', 'N/A')
    win_rate = response_body.get('win_rate', 'N/A')
    sharpe_ratio = response_body.get('sharpe_ratio', 'N/A')

    response += f"Balance: {balance}\n"
    response += f"Profit and Loss: {pnl}\n"
    response += f"Realized Profit and Loss: {realized_pnl}\n"
    response += f"Profit Factor: {profit_factor}\n"
    response += f"Win Rate: {win_rate}\n"
    response += f"Sharpe Ratio: {sharpe_ratio}\n"

    user_margin = response_body.get('user_margin', {})
    used_margin = user_margin.get('used', 'N/A')
    balance_margin = user_margin.get('balance', 'N/A')
    response += f"\nUser Margin:\n"
    response += f"Used Margin: {used_margin}\n"
    response += f"Balance Margin: {balance_margin}\n"

    return response

def respond_to_account_positions(response_body):
    response = f"Account Positions\n\n"

    positions = response_body.get('positions', [])
    if len(positions) == 0:
        return "You have no open positions at the moment"
    for position in positions:
        instrument_name = position.get('instrument_name', 'N/A')
        instrument_type = position.get('instrument_type', 'N/A')

        asset = position.get('asset', 'N/A')
        amount = position.get('amount', 'N/A')
        side = position.get('side', 'N/A')
        mark_price = position.get('mark_price', 'N/A')
        avg_entry_price = position.get('avg_entry_price', 'N/A')
        unrealized_pnl = position.get('unrealized_pnl', 'N/A')
        maintenance_margin = position.get('maintenance_margin', 'N/A')
        margin_type = position.get('margin_type', 'N/A')
        liquidation_price = position.get('liquidation_price', 'N/A')
        isolated_margin = position.get('isolated_margin', 'N/A')
        leverage = position.get('leverage', 'N/A')

        response += f"Asset: {asset}\n"
        response += f"Asset Ticker: {instrument_name}\n"
        response += f"Asset Type: {instrument_type}\n"
        response += f"Amount: {amount}\n"
        response += f"Trade Side: {side}\n"
        response += f"Mark Price: {mark_price}\n"
        response += f"Avg. Entry Price: {avg_entry_price}\n"
        response += f"Unrealized PNL: {unrealized_pnl}\n"
        response += f"Maintenance Margin: {maintenance_margin}\n"
        response += f"Margin Type: {margin_type}\n"
        response += f"Liquidation Price: {liquidation_price}\n"
        response += f"Isolated Margin: {isolated_margin}\n"
        response += f"Leverage: {leverage}\n"

        triggers = position.get('triggers', {})
        take_profit = triggers.get('take_profit', {})
        stop_loss = triggers.get('stop_loss', {})

        if take_profit:
            take_profit_order_id = take_profit.get('order_id', 'N/A')
            take_profit_trigger = take_profit.get('trigger', 'N/A')
            response += f"Take Profit Order ID: {take_profit_order_id}\n"
            response += f"Take Profit Trigger: ${take_profit_trigger}\n"

        if stop_loss:
            stop_loss_order_id = stop_loss.get('order_id', 'N/A')
            stop_loss_trigger = stop_loss.get('trigger', 'N/A')
            response += f"Stop Loss Order ID: {stop_loss_order_id}\n"
            response += f"Stop Loss Trigger: ${stop_loss_trigger}\n"

        response += "\n"

    return response
