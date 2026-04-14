from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    loans = db.relationship("LoanApplication", backref="applicant", lazy=True)


class LoanApplication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    applicant_income = db.Column(db.Float, nullable=False)
    credit_history = db.Column(db.Float, nullable=False)
    result = db.Column(db.String(20), nullable=False)
    probability = db.Column(db.Float, nullable=False)
    loan_amount = db.Column(db.Float, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def __repr__(self):
        return f"<LoanApplication {self.id}>"
    

