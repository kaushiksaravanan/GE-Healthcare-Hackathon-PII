from sqlalchemy import create_engine, MetaData, Table, exc

def get_all_values(user, password, host, database, engine_type="mysql"):
  """
  Retrieves all values from all tables and a list of dictionaries containing table names
  and their column names from a database, handling connection differences based on SQLAlchemy
  version and supporting both MySQL and PostgreSQL engines.

  Args:
      user (str): Username for the database.
      password (str): Password for the database.
      host (str): Hostname or IP address of the database server.
      database (str): Name of the database to connect to.
      engine_type (str, optional): Type of database engine ("mysql" or "postgres").
          Defaults to "mysql".

  Returns:
      tuple: A tuple containing two elements:
          1. list: A list of lists, where each inner list contains values from a single row in a table,
              or None if there's an error.
          2. list: A list of dictionaries, where each dictionary contains
              'table_name' and a list of 'column_names'.
  """
  # Warning: Using an empty password for database connections is insecure!
  print("WARNING: Using an empty password for database connections is insecure!")

  try:
    # Create connection string based on engine type
    if engine_type == "mysql":
      engine_string = f"mysql+pymysql://{user}:{password}@{host}/{database}"
    elif engine_type == "postgres":
      engine_string = f"postgresql://{user}:{password}@{host}/{database}"
    else:
      raise ValueError(f"Unsupported engine type: {e}")

    # Create the connection engine
    engine = create_engine(engine_string)
    print("Connected to database successfully!")  # For debugging

    # Create a connection from the engine (for SQLAlchemy 1.4+)
    connection = engine.connect() if hasattr(engine, 'connect') else engine

  except (exc.SQLAlchemyError, ValueError) as e:
    print(f"Error connecting to database: {e}")
    return None, None

  # Use reflection to get table information
  metadata = MetaData()
  metadata.reflect(engine)

  # List to store table information
  table_columns = []

  # Iterate through each table
  all_values = []
  for table_name, table in metadata.tables.items():
    print(f"Processing table: {table_name}")  # Print table name before processing

    # Get column names
    column_names = [column.name for column in table.columns]

    # Create dictionary and append to list
    table_info = {'table_name': table_name, 'column_names': column_names}
    table_columns.append(table_info)

    # Construct a select query to fetch all rows
    query = table.select()

    # Execute the query (using connection for SQLAlchemy 1.4+)
    results = connection.execute(query) if hasattr(engine, 'connect') else engine.execute(query)

    # Extract values from each row and append to all_values
    for row in results:
      all_values.append(list(row))

  # Close the connection (for SQLAlchemy 1.4+)
  if hasattr(engine, 'connect'):
    connection.close()

  return all_values, table_columns

# Example usage with MySQL credentials (insecure)
user = "postgres"               # MySQL: root, Postgres: postgres
password = "fazil"              # MySQL: , Postgres: fazil
host = "localhost:5432"         # MySQL: localhost:3306, Postgres: localhost:5432
database = "test"
engine_type = "postgres"        # MySQL: mysql, Postgres: postgres

all_values, table_columns = get_all_values(user, password, host, database, engine_type)

# Print table information and data (if any)
if table_columns:
  for info in table_columns:
    print(f"Table: {info['table_name']}, Columns: {info['column_names']}")
else:
  print("No tables found in the database.")

if all_values:
  for row in all_values[:5]:
    print(row)
else:
  print("No data found in the database.")
