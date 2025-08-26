from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
import logging
from datetime import datetime

# Select transport with defined url point
transport = AIOHTTPTransport( url="http://localhost:8000/graphql" )

# Create a client using the defined transport
client = Client( transport=transport )

# -------------------------- Query Section -----------------------------

query = gql(
    """
    query GetOrders($orderDateGte: Datetime!) {
        orders(orderDateGte: $orderDateGte) {
            id 
            customer {
                name
                email
            }
            products {
                name
                price
            }
            totalAmount
            orderDate
        }
    }
    """ 
)

# -----------------------------------------------------------------------

# Execute the query on the transport
result = client.execute( query )

# Process the result
logging.basicConfig( filename="/tmp/order_reminders_crontab.txt" )

# Log the order details to order_reminders_crontab.txt
# with open( "order_reminders_crontab.txt", "w" ) as file:
for order in result['orders']:
    logging.info( f"{datetime.now().isoformat()} - Order ID: {order['id']}, Customer Email: {order['customer']['email']}" )

    