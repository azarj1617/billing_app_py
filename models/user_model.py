from extensions import db

class User(db.Model):
    __tablename__ = 'users'  # make sure it matches your MySQL table name

    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.Date, nullable=False)

    def __repr__(self):
        return f"<User {self.name}>"

    def to_dict(self):
        return {
            "userId": self.user_id,
            "userName": self.user_name,
            "createdAt": self.created_at.strftime("%d-%m-%Y")
        }
