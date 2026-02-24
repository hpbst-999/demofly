import psycopg2
from psycopg2.pool import SimpleConnectionPool
from psycopg2.extras import RealDictCursor
from config import Config
db_pool = SimpleConnectionPool(
    minconn=1,
    maxconn=10,
    **Config.DB_CONFIG
)
def query_db(sql, params=None, fetchone=False):
    conn = db_pool.getconn()
    try:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(sql, params or ())
            if cur.description is None:
                conn.commit()
                return None
            if fetchone:
                return cur.fetchone()
            return cur.fetchall()
    except Exception as e:
        conn.rollback()
        raise e 
    finally:
        db_pool.putconn(conn)
# Нужно ли тут исполользовать commit/rollback если использую with as? https://pythonru.com/biblioteki/tranzakcii-postgres-v-python

