import psycopg2


def check_database_connection(params):
    try:
        with psycopg2.connect(**params) as conn:
            with conn.cursor():
                print("Connection to the database successful.")
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")


# Replace params with your actual database connection parameters
db_params = {
    'dbname': 'cw5',
    'user': 'postgres',
    'password': '12345',
    'host': 'localhost',
    'port': 5433
}

check_database_connection(db_params)
