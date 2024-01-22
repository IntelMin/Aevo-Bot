import re
import unicodedata
from decimal import Decimal
from datetime import datetime
from .blockchain import w3

def truncate_address(address, start_length=4, end_length=4):
    """
    Truncate an Ethereum address to make it shorter for display purposes.
    Example: 0x1234567890123456789012345678901234567890 -> 0x123456...567890
    """
    if not address.startswith("0x"):
        return address  # Return original if it doesn't look like an address

    return address[:start_length] + "..." + address[-end_length:]

def wei_to_eth(wei_value):
    """
    Convert a wei value to its equivalent in Ethereum.
    """
    eth_value = w3.from_wei(float(wei_value), 'ether')
    return eth_value

def round_to_decimals(value, decimal_places=6):
    """
    Round a number to a given number of decimal places.
    """
    multiplier = 10 ** decimal_places
    return Decimal(value * multiplier).quantize(1) / multiplier

def format_eth(value, decimal_places=6):
    """
    Convert wei to eth, then round it to the specified decimal places.
    """
    eth_value = wei_to_eth(value)
    return round_to_decimals(eth_value, decimal_places)

def pretty_timestamp(timestamp):
    """
    Convert a UNIX timestamp to a more human-readable format.
    """
    dt = datetime.utcfromtimestamp(timestamp)
    return dt.strftime('%Y-%m-%d %H:%M:%S')

def display_width(s):
    """
    Calculate the display width of a string, accounting for wide characters and emojis.
    """
    width = 0
    for char in s:
        if unicodedata.east_asian_width(char) in ['F', 'W']:
            width += 2
        else:
            width += 1
    return width


def generate_table(headers, data):
    """
    Generate a Markdown table from a list of headers and data.
    """
    # First, find the maximum width for each column
    col_widths = [display_width(header) for header in headers]

    for row in data:
        for idx, item in enumerate(row):
            col_widths[idx] = max(col_widths[idx], display_width(str(item)))

    # Create the header row using the computed column widths
    header_row = '   '.join([headers[i].ljust(col_widths[i]) for i in range(len(headers))])

    # Create the table rows
    table_rows = []
    for row in data:
        table_rows.append('   '.join([str(item).ljust(col_widths[idx]) for idx, item in enumerate(row)]))

    return "```\n" + header_row + "\n" + "\n".join(table_rows) + "\n```"

def format_large_number(n):
    if n < 1_000:
        return str(n)
    elif n < 1_000_000:
        return f"{n / 1_000:.1f}k".rstrip('0').rstrip('.')
    elif n < 1_000_000_000:
        return f"{n / 1_000_000:.1f}m".rstrip('0').rstrip('.')
    elif n < 1_000_000_000_000:
        return f"{n / 1_000_000_000:.1f}b".rstrip('0').rstrip('.')
    else:
        return f"{n / 1_000_000_000_000:.1f}t".rstrip('0').rstrip('.')
    
def extract_eth_address(subject):
    pattern = r"0x[a-fA-F0-9]{40}"
    match = re.search(pattern, subject)
    return match.group() if match else None