import sqlite3
import os
import pandas as pd
from datetime import datetime

conn = sqlite3.connect(f'{os.getcwd()}//db_repo//startups.db', check_same_thread = False)
cur = conn.cursor()

# add info to database
def add2db(table, columns, values):
    q_marks = str(tuple('?' for i in values)).replace("'", "")
    try:
        query = f"""
                INSERT INTO {table} {str(columns)} VALUES {q_marks}
                """
        cur.execute(query, values)
        conn.commit()
    except:
        raise Exception("The startup note is already in the database!")

# convert SQL database to .csv format
def convert_db2csv(table):
    df = pd.read_sql_query(f"SELECT * FROM {table}", conn)
    df.to_csv(f'startups_db_{datetime.now().strftime("%Y_%m_%d")}.csv')