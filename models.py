from flask_sqlalchemy import SQLAlchemy

# SQLAlchemy nesnesi oluştur
db = SQLAlchemy()

class Customer(db.Model):
    __tablename__ = 'customers'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    addr = db.Column(db.String(200))
    city = db.Column(db.String(100))
    pin = db.Column(db.String(20))
    phone = db.Column(db.String(20))

    def __repr__(self):
        return f'<Customer {self.name}>'
