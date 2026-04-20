import bcrypt
from app.models.user import User

class AuthService:
    def __init__(self, repo):
        self.repo = repo

    def verify_user(self, username, password):
        user = self.repo.get_by_username(username)
        if user and bcrypt.checkpw(password.encode(), user.password_hash.encode()):
            return user
        return None
