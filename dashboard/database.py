
from sqlalchemy import create_engine, URL
import pandas as pd

# MySQL database configuration
DB_USER = "root"
DB_PASSWORD = "WJ28@krhps"
DB_HOST = "localhost"
DB_PORT = 3306
DB_NAME = "ecommerce"

# Create a safe MySQL connection URL
# URL.create() handles special characters in passwords,
# such as @, #, %, and /.
connection_url = URL.create(
    drivername="mysql+mysqlconnector",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME
)

# Create SQLAlchemy engine
engine = create_engine(connection_url)


# Function to execute SQL queries and return a DataFrame
def get_data(query):
    return pd.read_sql(query, engine)
