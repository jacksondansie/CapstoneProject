from genericpath import exists
import sqlite3

def create_schema():
    connection = sqlite3.connect('Competency_Tracking_Tool.db')
    db_cursor = connection.cursor()
    with open ('table_text.txt') as schema:
        queries = schema.read()

        db_cursor.executescript(queries)
    connection.commit()

create_schema()
