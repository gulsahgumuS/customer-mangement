from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from models import db, Customer  # models.py dosyasını içe aktar

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()  # Tabloları oluştur


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/enternew')
def new_customer():
    return render_template('customer.html')

@app.route('/addrec', methods=['POST', 'GET'])
def addrec():
    if request.method == 'POST':
        try:
            nm = request.form['nm']
            addr = request.form['add']
            city = request.form['city']
            pin = request.form['pin']
            phone = request.form['phone']

            new_customer = Customer(name=nm, addr=addr, city=city, pin=pin, phone=phone)
            db.session.add(new_customer)
            db.session.commit()
            msg = "Record successfully added"
        except Exception as e:
            db.session.rollback()
            msg = f"Error in insert operation: {e}"
        finally:
            return render_template("result.html", msg=msg)

@app.route('/list')
def list_customers():
    customers = Customer.query.all()  # Tüm müşterileri al
    return render_template("list.html", rows=customers)

if __name__ == '__main__':
    app.run(debug=True)
