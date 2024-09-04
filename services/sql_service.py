import sqlite3
import pandas as pd
import services.logging_service as log

def run_sql_query(data_frame: pd.DataFrame, query: str):
     # Create a connection to SQLite (in-memory)
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # Write the DataFrame to the SQLite database
    data_frame.to_sql('company_info', conn, index=False, if_exists='replace')

    # Execute the query and fetch the results
    log.info("Function - run_sql_query - Done")
    results = pd.read_sql_query(query, conn)
    conn.close()
    return results
