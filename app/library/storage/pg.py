# import os

# from google.cloud.sql.connector import Connector, IPTypes
# import pg8000

# import sqlalchemy
# from sqlalchemy.orm import declarative_base

# # Define the base for declarative models
# Base = declarative_base()

# def connect_with_connector() -> sqlalchemy.engine.base.Engine:
#     """
#     Initializes a connection pool for a Cloud SQL instance of Postgres.

#     Uses the Cloud SQL Python Connector package.
#     """
#     # Note: Saving credentials in environment variables is convenient, but not
#     # secure - consider a more secure solution such as
#     # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
#     # keep secrets safe.

#     instance_connection_name = os.environ[
#         "INSTANCE_CONNECTION_NAME"
#     ]  # e.g. 'project:region:instance'
#     db_user = os.environ["DB_USER"]  # e.g. 'my-db-user'
#     db_pass = os.environ["DB_PASS"]  # e.g. 'my-db-password'
#     db_name = os.environ["DB_NAME"]  # e.g. 'my-database'

#     ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC

#     # initialize Cloud SQL Python Connector object
#     connector = Connector(refresh_strategy="LAZY")

#     def getconn() -> pg8000.dbapi.Connection:
#         conn: pg8000.dbapi.Connection = connector.connect(
#             instance_connection_name,
#             "pg8000",
#             user=db_user,
#             password=db_pass,
#             db=db_name,
#             ip_type=ip_type,
#         )
#         return conn

#     # The Cloud SQL Python Connector can be used with SQLAlchemy
#     # using the 'creator' argument to 'create_engine'
#     pool = sqlalchemy.create_engine(
#         "postgresql+pg8000://",
#         creator=getconn,
#         # ...
#     )
#     return pool

# class PGDataBase:
#     def __init__(self, pool: sqlalchemy.Engine):
#         self.pool = pool
#     def query(self, query: str):
#         with self.pool.connect() as db:
#             result = db.execute(sqlalchemy.text(query))
#             return result.all()
