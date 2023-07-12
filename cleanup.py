import os
import json
import logging
from crate import client
from datetime import datetime
from sys import stdout

# Set up logging
logging.basicConfig(level=logging.INFO, handlers=[logging.StreamHandler(stdout)])

# Load the configuration
try:
    with open("./config.json") as json_file:
        config = json.load(json_file)
except Exception as e:
    logging.error(f"Error loading configuration: {e}")
    raise


def delete_old_records(table, time_index, duration):
    try:
        connection = client.connect(os.getenv('CRATE_HOST'), username=os.getenv('CRATE_USER'), password=os.getenv('CRATE_PASSWORD'))
        cursor = connection.cursor()
        
        # Extract number and unit from the duration
        num, unit = int(duration[:-1]), duration[-1]
        
        # Convert the unit to a format acceptable by CrateDB's interval function
        units_map = {"s": "second", "m": "minute", "h": "hour", "d": "day"}
        unit = units_map.get(unit)

        # Form the SQL query
        query = f"DELETE FROM {table} WHERE {time_index} < CURRENT_TIMESTAMP - INTERVAL '{num} {unit}'"
        
        cursor.execute(query)
        connection.commit()
        logging.info(f'Successfully deleted records older than {duration} from {table}')
    except Exception as e:
        logging.error(f'Error deleting records from {table}: {e}')



for table, attrs in config.items():
    delete_old_records(table, attrs["time-index"], attrs["retention"])
