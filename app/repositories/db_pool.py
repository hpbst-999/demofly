import psycopg2
from psycopg2.pool import SimpleConnectionPool
from config import Config

db_pool = SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    **Config.DB_CONFIG
)
