import psycopg2 as psql
from config import config
import traceback, json

def execute(command, po=False):
    global connection, cursor
    if po:
        print(command)
    cursor.execute(command)
    if command.upper().startswith("SELECT"):
        results = cursor.fetchall()
        if po:
            print("\t", results)
        else:
            return results
    else:
        connection.commit()

def main(connection, cursor):
    print("There are", execute("select count(*) from movies")[0][0], "entries in the table.")
    execute("delete from sample_statements") # empty the table before adding the new tuples

    # add sample statements
    command = "insert into sample_statements values "
    with open("sample_statements.json") as f:
        statements = [obj["body"] for obj in json.load(f)["data"]]
    for s in statements:
        s = s.replace("'", "''").replace("\n", "  ")
        command += fr"('{s}'), "
    command = command[:-2] # get rid of extra ', '
    execute(command, po=False)

    # verify that the new tuples have been added
    execute("select body from sample_statements where body like '%Saints%'", po=True)

def connect():
    """Connect to the PostgreSQL database server"""
    conn = None
    try:
        params = config()
        print('Connecting to the PostgreSQL database')
        conn = psql.connect(**params)
        cur = conn.cursor()
        print("PostgreSQL Database Version:")
        cur.execute("SELECT version()")
        db_version = cur.fetchone()
        print(db_version[0])

        return conn, cur
    
    except (Exception, psql.DatabaseError) as error:
        print(error)
        if conn is not None:
            conn.close()
            print("Database connection closed due to error.")

if __name__ == "__main__":
    connection, cursor = connect()
    try:
        main(connection, cursor)
    except:
        traceback.print_exc()
    finally:
        print("...Program Execution Completed / Error (Closing database connection)...")
        cursor.close()
        connection.close()