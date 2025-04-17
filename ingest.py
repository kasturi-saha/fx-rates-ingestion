import requests
import duckdb
import logging
import os
from datetime import datetime

"""
This file ingests fx rates from the https://openexchangerates.org/ free API and inserts into a source table
"""

logging.basicConfig(level=logging.INFO)


def get_API_KEY():
    """
    returns API key from the ENV variables
    :return: API key
    """
    api_key = os.getenv("API_KEY")
    if not api_key:
        logging.error("Missing API_KEY environment variable.")
        return
    return api_key


def fetch_and_store_raw_rates():
    """
    1. Fetches fx rates from the https://openexchangerates.org/
    2. Creates a new table if it does not exist
    3. Inserts the fx rates data into the table
    :return:
    """
    try:
        # Fetch data from the API
        response = requests.get(f"https://openexchangerates.org/api/latest.json?app_id={get_API_KEY()}", timeout=10)
        response.raise_for_status()
        data = response.json()

        rates = data.get("rates")
        if not rates:
            raise ValueError("Missing 'rates' in API response.")

        if "CAD" not in rates:
            raise ValueError("CAD rate not found in response.")

        # Transform JSON to rows suitable for DB
        rows = [(data["timestamp"], currency, rate) for currency, rate in rates.items()]

        # Open new duckDB connection
        with duckdb.connect("fx_data.duckdb") as con:
            # Create a new table if it does not already exist
            con.execute("""
                CREATE TABLE IF NOT EXISTS raw_fx_rates_usd_base (
                    timestamp INTEGER,
                    currency TEXT,
                    rate DOUBLE
                )
            """)

            # Insert the fx data into the source table
            con.executemany("""
                INSERT INTO raw_fx_rates_usd_base (timestamp, currency, rate) VALUES (?, ?, ?)
            """, rows)

        logging.info(f"Fetched and stored FX rates for {datetime.utcfromtimestamp(data['timestamp'])}.")

    except requests.RequestException as e:
        logging.error(f"API request failed: {e}")
    except Exception as e:
        logging.error(f"Error: {e}")


if __name__ == "__main__":
    fetch_and_store_raw_rates()
