import logging
from celery import shared_task
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime
from gql import (
    gql,
    Client,
    GraphQLRequest
)
import requests


@shared_task
def generate_crm_report():
    request = gql(
        """
            query {
                totalCustomers
                totalOrders
                totalRevenue
            }   
        """ 
    )
    
    transport = RequestsHTTPTransport(
        url="http://localhost:8000/graphql",
        verify=True,
        retries=3,
    )

    client = Client( transport=transport )

    result = client.execute( request=request )

    logging.basicConfig(filename="/tmp/crm_report_log.txt")

    # YYYY-MM-DD HH:MM:SS - Report: X customers, Y orders, Z revenue.
    data = result['data']
    number_of_customers = data['totalCustomers']
    number_of_orders = data['totalOrders']
    current_total_revenue = data['totalRevenue']

    logging.info( f"{datetime.now().isoformat()} - \
                 Report: \
                 {number_of_customers} customers, \
                    {number_of_orders} orders, \
                        {current_total_revenue} revenue." )
    


if __name__ == "__main__":
    pass