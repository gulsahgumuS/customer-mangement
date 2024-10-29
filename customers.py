from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)
    addr = db.Column(db.String)
    city = db.Column(db.String)
    pin = db.Column(db.String)
    phone = db.Column(db.String)

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

            new_customer = Customer(name=nm, addr=addr, city=city, pin=pin)
            db.session.add(new_customer)
            db.session.commit()
            return redirect(url_for('list_customer'))
        except Exception as e:
            db.session.rollback()
            return redirect(url_for('list_customer'))

@app.route('/list')
def list_customer():
    customer = Customer.query.all()
    return render_template("list.html", rows=customer)

@app.route('/delete/<int:id>', methods=['POST'])
def delete_customer(id):
    customer_to_delete = Customer.query.get_or_404(id)
    try:
        db.session.delete(customer_to_delete)
        db.session.commit()
        
        # Tüm tabloyu yenileyen güncel listeyi döndürür
        customers = Customer.query.all()
        return render_template("list.html", rows=customers)
    except Exception as e:
        db.session.rollback()
        return redirect(url_for('list_customer'))


if __name__ == '__main__':
    app.run(debug=True)
