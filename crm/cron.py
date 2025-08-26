import logging
from datetime import datetime

def log_crm_heartbeat():
    logging.basicConfig( filename="/tmp/crm_heartbeat_log.txt" )

    # DD/MM/YYYY-HH:MM:SS CRM is alive
    logging.info( f"{datetime.now().isoformat()} CRM is alive" )

