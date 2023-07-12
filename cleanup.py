import os
import json
import logging
from crate import client
from datetime import datetime

# Set up logging
logging.basicConfig(filename="/app/cleanup.log", level=logging.INFO)

# Load the configuration
try:
    with open("/app/config.json") as json_file:
        config = json.load(json_file)
except Exception as e:
    logging.error(f"Error loading configuration: {e}")
    raise


def delete_old_records(table, time_index, duration):
    try:
        connection = client.connect(
            os.getenv("CRATE_HOST"),
            username=os.getenv("CRATE_USER"),
            password=os.getenv("CRATE_PASSWORD"),
        )
        cursor = connection.cursor()
        query = f"DELETE FROM {table} WHERE {time_index} < CURRENT_TIMESTAMP - INTERVAL '{duration}'"
        cursor.execute(query)
        connection.commit()
        logging.info(f"Successfully deleted records older than {duration} from {table}")
    except Exception as e:
        logging.error(f"Error deleting records from {table}: {e}")


for table, attrs in config.items():
    delete_old_records(table, attrs["time-index"], attrs["retention"])
