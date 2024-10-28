from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)

def create_table():
    with sql.connect("database.db") as con:
        cur = con.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            addr TEXT,
            city TEXT,
            pin TEXT
        )
        """)
        con.commit()

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
            
            with sql.connect("database.db") as con:
                cur = con.cursor()
                cur.execute("INSERT INTO customers (name, addr, city, pin) VALUES (?, ?, ?, ?)", (nm, addr, city, pin))
                con.commit()
                
            # Ekleme işlemi tamamlandıktan sonra müşteri listesini döndür
            con.row_factory = sql.Row
            cur = con.cursor()
            cur.execute("SELECT * FROM customers")
            rows = cur.fetchall()
            return render_template("list.html", rows=rows)
            
        except Exception as e:
            con.rollback()
            msg = f"Error in insert operation: {e}"
            return render_template("result.html", msg=msg)
        finally:
            con.close()

@app.route('/list')
def list_customers():
    with sql.connect("database.db") as con:
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM customers")
        rows = cur.fetchall()
    return render_template("list.html", rows=rows)

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
