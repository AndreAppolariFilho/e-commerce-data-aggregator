import os
from functools import wraps

from flask import Flask, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("APPLICATION_SECRET_KEY", "SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DB_URL", f'sqlite:///{os.path.join(os.getcwd(), "db", "store.db")}')
app.config["JWT_SECRET_KEY"] = os.environ.get("APPLICATION_JWT_SECRET_KEY", 'your_jwt_secret_key')
db = SQLAlchemy(app)


class Sale(db.Model):
    __tablename__ = "sale"
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.Text, nullable=False)
    price = db.Column(db.Numeric(precision=10, scale=2), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "product_name": self.product_name,
            "price": self.price,
            "quantity": self.quantity,
            "created_at": self.created_at
        }


@app.route("/monthly_sales", methods=["GET"])
def monthly_sales_list_api_view():
    if request.method == "GET":
        results = db.session.query(
            func.extract('year', Sale.created_at).label('year'),
            func.extract('month', Sale.created_at).label('month'),
            func.sum(Sale.price).label('total_price')
        ).group_by(
            func.extract('year', Sale.created_at),
            func.extract('month', Sale.created_at)
        ).all()
        return jsonify(
            [
                {
                    "date": f"{result.month}/{result.year}",
                    "price": result.total_price
                } for result in results
            ]
        ), 200


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True, host="0.0.0.0", port=os.environ.get("port", "5003"))
