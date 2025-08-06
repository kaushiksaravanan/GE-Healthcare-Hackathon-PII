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
    elif engine_type == "sqlite":
      # SQLite doesn't use user/password
      engine_string = f"sqlite:///{host}/{database}"  # Assuming database is a file
      engine_string = f"sqlite:///D:/Hackathons/GE Healthcare/GE-Healthcare-Hackathon/testing/database_dumb_dir/test.db"
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

def fun(database_type, database_host, database_name, database_user, database_password):

    if (database_type == "sqlite"):
        # Example usage with MySQL credentials (insecure)
        user = ""               # MySQL: root, Postgres: postgres, SQLite:
        password = ""              # MySQL: , Postgres: fazil, SQLite:
        host = "D:/Hackathons/GE Healthcare/GE-Healthcare-Hackathon/testing/database_dumb_dir"         # MySQL: localhost:3306, Postgres: localhost:5432, SQLite: D:/Hackathons/GE Healthcare/GE-Healthcare-Hackathon/testing/database_dumb_dir
        database = "test.db"               # MySQL & Postgres: test, Sqlite: test.db
        engine_type = database_type        # MySQL: mysql, Postgres: postgres, SQLite: sqlite
    if (database_type == "mysql"):
        # Example usage with MySQL credentials (insecure)
        user = "mysql"               # MySQL: root, Postgres: postgres, SQLite:
        password = "fazil"              # MySQL: , Postgres: fazil, SQLite:
        host = "localhost:3306"         # MySQL: localhost:3306, Postgres: localhost:5432, SQLite: D:/Hackathons/GE Healthcare/GE-Healthcare-Hackathon/testing/database_dumb_dir
        database = "test"               # MySQL & Postgres: test, Sqlite: test.db
        engine_type = database_type        # MySQL: mysql, Postgres: postgres, SQLite: sqlite
    if (database_type == "postgres"):
        # Example usage with MySQL credentials (insecure)
        user = "postgres"               # MySQL: root, Postgres: postgres, SQLite:
        password = "fazil"              # MySQL: , Postgres: fazil, SQLite:
        host = "localhost:5432"         # MySQL: localhost:3306, Postgres: localhost:5432, SQLite: D:/Hackathons/GE Healthcare/GE-Healthcare-Hackathon/testing/database_dumb_dir
        database = "test"               # MySQL & Postgres: test, Sqlite: test.db
        engine_type = database_type        # MySQL: mysql, Postgres: postgres, SQLite: sqlite

    user = database_user
    password = database_password
    host = database_host
    database = database_name
    engine_type = database_type

    all_values, table_columns = get_all_values(user, password, host, database, engine_type)

    response = ""
    response += database_type 

    # Print table information and data (if any)
    if table_columns:
        for info in table_columns:
            response += "\nTable: " + str(info['table_name']) + ", Columns: " + str(info['column_names']) + ""
    else:
        response += "\nNo tables found in the database."

    if all_values:
        for row in all_values:
            response += "\n" + str(row)
    else:
        response += "\nNo data found in the database."

    return response
