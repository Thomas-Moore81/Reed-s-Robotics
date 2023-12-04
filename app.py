from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

@app.route('/')
def index():
    db_config = {
    'host': 'dbdev.cs.kent.edu',
    'user': 'lsimps14',
    'password': 'of67DKid',
    'database': 'lsimps14',
    }

    connection = mysql.connector.connect(**db_config)

    #connection._execute_query("INSERT INTO customers (customer_id, customer_name, customer_address, customer_email) VALUES(1, 'lane', '123 sesame st', 'lane@mail.com')")
    #connection.commit()
    
    db_Info = connection.get_server_info()
    print("Connected to MySQL Server version ", db_Info)
    connection.close()
    return render_template('landing_page.html')

@app.route('/dashboard.html', methods=['GET', 'POST'])
def dashboard():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Add your authentication logic here
        # For demonstration purposes, redirect to 'dashboard' without authentication
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
    # In a real app, you would fetch past_repairs from your database
    past_repairs = [
        {"ticket_id": 1, "robot_id": 101, "condition": "Broken", "repair_location": "Repair Center", "technician": "John Doe", "part_id": "P123"},
        # Add more repair entries as needed
    ]
    return render_template('repairs.html', past_repairs=past_repairs)

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5006)

# from flask import Flask, render_template, request, redirect, url_for
# import mysql.connector

# app = Flask(__name__)

# # replace these with the database stuff for whoever is doing the database
# db_config = {
#     'host': 'dbdev.cs.kent.edu',
#     'user': 'lsimps14',
#     'password': 'of67DKid',
#     'database': 'lsimps14'
# }

# def fetch_past_repairs():
#     past_repairs = []
#     connection = None
#     try:
#         connection = mysql.connector.connect(**db_config)
#         cursor = connection.cursor(dictionary=True)

#         cursor.execute("SELECT * FROM repairs")
#         past_repairs = cursor.fetchall()

#         return past_repairs

#     except mysql.connector.Error as err:
#         print(f"Error: {err}")
#         return []

#     finally:
#         if connection and connection.is_connected():
#             cursor.close()
#             connection.close()
    
#     return past_repairs

# @app.route('/')
# def index():
#     past_repairs = fetch_past_repairs()
#     return render_template('orders.html', past_repairs=past_repairs)

# @app.route('/submit_repair', methods=['POST'])
# def submit_repair():
#     robot_id = request.form['robot_id']
#     condition = request.form['condition']
#     repair_location = request.form['repair_location']
#     technician = request.form['technician']
#     part_id = request.form['part_id']

#     add_repair_to_database(robot_id, condition, repair_location, technician, part_id)

#     # Redirect to the home page after submitting the repair
#     return redirect(url_for('index'))

# def add_repair_to_database(robot_id, condition, repair_location, technician, part_id):
#     try:
#         connection = mysql.connector.connect(**db_config)
#         cursor = connection.cursor()

#         add_repair_query = "INSERT INTO repairs (robot_id, condition, repair_location, technician, part_id) " \
#         "VALUES (%s, %s, %s, %s, %s)"
#         cursor.execute(add_repair_query, (robot_id, condition, repair_location, technician, part_id))
#         connection.commit()

#         print("processing...")

#     except mysql.connector.Error as err:
#         print(f"Error: {err}")

#     finally:
#         if connection.is_connected():
#             cursor.close()
#             connection.close()

# if __name__ == '__main__':
#     app.run(debug=True)