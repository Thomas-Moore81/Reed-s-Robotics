from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

db_config = {
    'host': 'dbdev.cs.kent.edu',
    'user': 'lsimps14',
    'password': 'of67DKid',
    'database': 'lsimps14',
}  

app = Flask(__name__)

@app.route('/')
def index():
    connection = mysql.connector.connect(**db_config)
    db_Info = connection.get_server_info()
    print("Connected to MySQL Server version ", db_Info)
    connection.close()
    return render_template('landing_page.html')

@app.route('/dashboard.html', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        return redirect(url_for('dashboard'))

    return render_template('dashboard.html')

@app.route('/orders')
def orders():
    return render_template('orders.html')

@app.route('/purchase_page')
def purchase_page():
    return render_template('purchase_page.html')

@app.route('/repairs')
def repairs():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    cursor.execute("SELECT * FROM Repairs")
    past_repairs = cursor.fetchall()
    return render_template('repairs.html', past_repairs=past_repairs)

@app.route('/submit_repair', methods=['POST'])
def update_repair():
    robot_id = request.form.get('robot_id')
    condition = request.form.get('condition')
    repair_location = request.form.get('repair_location')
    technician = request.form.get('technician')
    part_id = request.form.get('part_id')
    ticket_id = request.form.get('ticket_id')

    query = """
        UPDATE Repairs
        SET robot_id = %s, condition_type = %s, repair_location = %s, technician = %s, part_id = %s
        WHERE ticket_id = %s
    """
    data = (robot_id, condition, repair_location, technician, part_id, ticket_id)

    return execute_query(query, data)




def execute_query(query, data=None):
    db = mysql.connector.connect(**db_config)
    cursor = db.cursor()

    try:
        cursor.execute(query, data)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        cursor.close()
        db.close()

    return "Query executed successfully"



if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5006)
