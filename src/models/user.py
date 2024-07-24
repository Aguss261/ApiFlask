import bcrypt

class User:
    def __init__(self, id, username, email, password_hash, direccion,rol_id, created_at=None, updated_at=None):
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.direccion = direccion
        self.created_at = created_at
        self.updated_at = updated_at
        self.rol_id  = rol_id

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'direccion': self.direccion,
            "rol_id" : self.rol_id,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
