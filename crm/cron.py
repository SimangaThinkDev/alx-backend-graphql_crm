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

def sample_test_query( endpoint:str, request_query:GraphQLRequest ):
    transport = RequestsHTTPTransport(
        url=endpoint,
        verify=True,
        retries=3,
    )

    client = Client(transport=transport, fetch_schema_from_transport=True)

    result = client.execute(request_query)

if __name__ == "__main__":
    
    endpoint = "http://localhost:8000/graphql"
    request_query = gql(
        """
        query {
            hello
        }
        """
    )

    sample_test_query( endpoint=endpoint, request_query=request_query )
