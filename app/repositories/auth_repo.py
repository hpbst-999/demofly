from app.models.user import User
from psycopg2.extras import RealDictCursor

class AuthRepository:
    def __init__(self, db):
        self.db = db 

    def get_by_username(self, username):
        sql = "SELECT id, username, password_hash, role FROM users WHERE username = %s"
        param = [username]
        conn = self.db.getconn()  
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cur:
                cur.execute(sql, param)
                res = cur.fetchone()  
        finally:
            self.db.putconn(conn)  
        
        if res:
            return User(**res)
        return None