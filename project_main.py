"""
Database Management Systems - Prof. Scharff (Summer 2021)
Final Project
Alex ONeill
Maryia Kalodkina
"""
import psycopg2
from configparser import ConfigParser

# SECTION: FUNCTIONS
def config(filename='./database.ini', section='postgres'):
    """
    Ingests database connection parameters with masked credentials from a database.ini file in the below format:
        [postgres]
        host=localhost
        database=database_name
        user=username
        password=password
    """
    parser = ConfigParser()
    parser.read(filename)
    db_config = {}
    for param in parser.items(section):
        db_config[param[0]] = param[1]
    return db_config


def connect(con_str):
    """Establishes connection to the database"""
    try:
        connection = psycopg2.connect(**con_str)
        return connection
    except Exception as conn_err:
        print(conn_err)
        print('Unable to connect to database. Aborting')


# SECTION: MAIN
params = config()
conn = connect(params)
cur = conn.cursor()

if conn:
    try:
        # NOTE: Set to serialize for transaction ISOLATION
        conn.set_isolation_level(3)

        # NOTE: No autocommit to instill ATOMICITY
        conn.autocommit = False

        cur.execute("""
            ALTER TABLE Stock DROP CONSTRAINT fk_stock_depot;
            
            ALTER TABLE Stock ADD CONSTRAINT dep_id_cascade
            FOREIGN KEY(depid) REFERENCES Depot ON UPDATE CASCADE;
            
            UPDATE depot SET depid = 'dd1'WHERE depid = 'd1';
            """)
        
    except (Exception, psycopg2.DatabaseError) as err:
        print(err)
        print("Transactions could not be completed so database will be rolled back before start of transactions")
        conn.rollback()
    finally:
        # NOTE: Committed transaction = DURABILITY
        conn.commit()
        cur.close
        conn.close
        print("PostgreSQL connection is now closed")