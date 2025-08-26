import logging
from datetime import datetime
from gql.transport.requests import RequestsHTTPTransport
from gql import (
    gql,
    Client,
    GraphQLRequest
)


def log_crm_heartbeat():
    logging.basicConfig( filename="/tmp/crm_heartbeat_log.txt" )

    # DD/MM/YYYY-HH:MM:SS CRM is alive
    logging.info( f"{datetime.now().isoformat()} CRM is alive" )

def sample_test_query( endpoint:str ):
    transport = RequestsHTTPTransport(
        url=endpoint,
        verify=True,
        retries=3,
    )

    request_query = gql(
        """
        query {
            hello
        }
        """
    )

    client = Client(transport=transport, fetch_schema_from_transport=True)

    result = client.execute(request_query)

def update_low_stock( endpoint:str ):
    """
    Executes the UpdateLowStockProducts mutation via the GraphQL endpoint.
    
    Logs updated product names and new stock levels to 
    /tmp/low_stock_updates_log.txt with a timestamp.
    """

    mutation_string = gql(
        """
        mutation {
          updateLowStockProducts {
            message
            updatedProducts {
              id
              name
              stock
            }
          }
        }
    """
    )

    transport = RequestsHTTPTransport(
        url=endpoint,
        verify=True,
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=True)

    try:
        # Execute the mutation
        response = client.execute(mutation_string)
        
        # Access the returned data
        message = response['updateLowStockProducts']['message']
        updated_products = response['updateLowStockProducts']['updatedProducts']

        logging.basicConfig( filename="/tmp/low_stock_updates_log.txt" )

        # DD/MM/YYYY-HH:MM:SS CRM is alive
        logging.info( f"Message: {message}\nUpdated Products: {updated_products}" )

    except Exception as e:
        print( "An error occured while trying to update low stock\
               contact developer immediately" )
    

if __name__ == "__main__":

    endpoint = "http://localhost:8000/graphql"
    # --------------------- Execute test hello query -------------------------------

    sample_test_query( endpoint=endpoint )

    # --------------------- Execute update low stock mutation -----------------------
    

