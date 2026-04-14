from flask import Blueprint, render_template
from .ml_model import predict_loan
from flask import request
from .models import LoanApplication
from . import db
main = Blueprint("main", __name__)
from .models import  User
from flask import session, redirect
from werkzeug.security import generate_password_hash, check_password_hash



@main.route("/")
def home():
    if "user_id" in session:
        user = User.query.get(session["user_id"])
        return render_template("index.html", user=user)

    return render_template("index.html")


# @main.route("/predict", methods=["POST"])
# def predict():
#     data = request.form.to_dict()
#     prediction, probability = predict_loan(data)

#     return render_template(
#         "result.html",
#         prediction="Approved" if prediction == 1 else "Rejected",
#         probability=f"{probability:.2%}",
#     )
# @main.route("/predict", methods=["POST"])
# def predict():
#     data = {
#         "ApplicantIncome": float(request.form.get("income")),
#         "Credit_History": float(request.form.get("credit_score"))
#     }

#     result, prob = predict_loan(data)

#     if result == 1:
#         output = "Approved"
#     else:
#         output = "Rejected"

#     return f"{output} (Confidence: {prob:.2f})"
@main.route("/predict", methods=["GET"])
def predict_page():
    return render_template("predict.html")
   

@main.route("/predict", methods=["POST"])
def predict():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session.get("user_id")

    income = float(request.form.get("ApplicantIncome"))
    credit = float(request.form.get("Credit_History"))

    data = {
        "ApplicantIncome": income,
        "Credit_History": credit
    }

    result, prob = predict_loan(data)

    # 🔥 BUSINESS RULE
    if credit == 0:
        result = 0
        prob = 0.0

    estimated_loan = income * 10

    # 🔥 SAVE TO DB
    loan = LoanApplication(
        applicant_income=income,
        credit_history=credit,
        result="Approved" if result == 1 else "Rejected",
        probability=prob,
        loan_amount=estimated_loan,
        user_id=user_id
    )

    db.session.add(loan)
    db.session.commit()

    return render_template(
        "result.html",
        prediction="Approved" if result == 1 else "Rejected",
        probability=f"{prob:.2%}",
        income=income,
        loan_amount=estimated_loan
    )


@main.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            session["user_id"] = user.id
            return redirect("/")

    return render_template("login.html")

@main.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/")
    


@main.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            return "Email already registered. Please login."

        hashed_password = generate_password_hash(password)

        new_user = User(
            username=name,   # 🔥 FIXED
            email=email,
            password_hash=hashed_password
        )

        db.session.add(new_user)
        db.session.commit()
        session["user_id"] = new_user.id

        return redirect("/")

    return render_template("register.html")


@main.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    loans = LoanApplication.query.filter_by(
        user_id=session["user_id"]
    ).order_by(LoanApplication.id.desc()).all()

    return render_template("dashboard.html", loans=loans)

   
