from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///employees.db'
app.secret_key = "supersecretkey"  # Used for flashing messages
db = SQLAlchemy(app)

def populate_sample_data():
    """Add sample employees to the database."""
    sample_employees = [
        {"name": "John Doe", "position": "Software Engineer", "email": "john.doe@example.com", "password": "password123"},
        {"name": "Jane Smith", "position": "Product Manager", "email": "jane.smith@example.com", "password": "password456"},
        {"name": "Robert Brown", "position": "System Administrator", "email": "robert.brown@example.com", "password": "securepass1"},
        {"name": "Lucy White", "position": "UX Designer", "email": "lucy.white@example.com", "password": "p@ssw0rd"},
        {"name": "Michael Johnson", "position": "Frontend Developer", "email": "michael.j@example.com", "password": "webdev123"},
        {"name": "Sarah Miller", "position": "Data Analyst", "email": "sarah.m@example.com", "password": "datascience"},
        {"name": "David Lee", "position": "Project Manager", "email": "david.l@example.com", "password": "project123"},
        {"name": "Amanda Wilson", "position": "Marketing Specialist", "email": "amanda.w@example.com", "password": "marketer"},
        #... continue for other employees
    ]

    for emp in sample_employees:
        new_employee = Employee(name=emp["name"], position=emp["position"], email=emp["email"], password=emp["password"])
        db.session.add(new_employee)
    db.session.commit()



class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    position = db.Column(db.String(80))
    email = db.Column(db.String(80))
    password = db.Column(db.String(80))  # New password field


@app.route('/')
def index():
    employees = Employee.query.all()
    return render_template('index.html', employees=employees)

@app.route('/add_employee', methods=['POST'])
def add_employee():
    name = request.form.get('name')
    position = request.form.get('position')
    email = request.form.get('email')
    new_employee = Employee(name=name, position=position, email=email)
    db.session.add(new_employee)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/search', methods=['POST'])
def search():
    query = request.form.get('query')
    
    # Intentionally vulnerable query
    connection = db.engine.connect()
    sql = text(f"SELECT email FROM employee WHERE name LIKE '%{query}%'")
    results = connection.execute(sql)
    emails = [row[0] for row in results]
    
    connection.close()
    return render_template('search_results.html', emails=emails)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create tables if they don't exist
        if Employee.query.count() == 0:
            populate_sample_data()
    app.run(debug=True, use_reloader=False)



