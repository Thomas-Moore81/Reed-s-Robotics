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

@app.route('/customers')
def customer_form():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM customers")
    current_customers = cursor.fetchall()
    return render_template('customers.html', current_customers=current_customers)

@app.route('/submit_customer', methods=['POST'])
def submit_customer():
    customer_id = request.form.get('customer_id')
    customer_name = request.form.get('customer_name')
    customer_address = request.form.get('customer_address')
    customer_email = request.form.get('customer_email')
    order_id = request.form.get('order_id')

    query = """
        INSERT INTO customers (customer_id, customer_name, customer_address, customer_email, order_id)
        VALUES (%s, %s, %s, %s, %s)
    """
    data = (customer_id, customer_name, customer_address, customer_email, order_id)

    try:
        execute_query(query, data)
        return f"Customer information submitted successfully: {customer_name}, {customer_address}, {customer_email}"
    except Exception as e:
        return f"Error submitting customer information: {str(e)}"

@app.route('/delete_customer', methods=['POST'])
def delete_customer():
    customer_id = request.form.get('customer_id')
    query = """
    DELETE FROM customers
    WHERE customer_id = %s
    """
    data = (customer_id,)
    try:
        execute_query(query, data)
        print(f"Customer deleted successfully.")
        return redirect(url_for('customer_form'))
    except Exception as e:
        print(f"Error deleting customer: {str(e)}")

@app.route('/delete_repair', methods=['POST'])
def delete_repair():
    ticket_id = request.form.get('ticket_id')
    query = """
    DELETE FROM Repairs
    WHERE ticket_id = %s
    """
    data = (ticket_id,)
    try:
        execute_query(query, data)
        print(f"Ticket deleted successfully.")
        return redirect(url_for('repairs'))
    except Exception as e:
        print(f"Error deleting ticket: {str(e)}")

@app.route('/orders')
def orders():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
    SELECT 
    c.customer_id,
    c.customer_name,
    c.customer_address,
    c.customer_email,
    r.robot_id,
    o.order_id
        FROM customers c
        LEFT JOIN orders o ON c.order_id = o.order_id
        LEFT JOIN robots r ON o.robot_id = r.robot_id;
""")
    orders = cursor.fetchall()
    return render_template('orders.html', orders=orders)


@app.route('/purchase_page')
def purchase_page():
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
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

    # Check if a record with the same robot_id and ticket_id already exists
    check_query = "SELECT * FROM Repairs WHERE robot_id = %s AND ticket_id = %s"
    check_data = (robot_id, ticket_id)

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    cursor.execute(check_query, check_data)
    existing_record = cursor.fetchone()
    connection.close()

    if existing_record:
        # If the condition is different, update the existing record
        if existing_record['condition_type'] != condition:
            update_query = """
                UPDATE Repairs
                SET condition_type = %s, repair_location = %s, technician = %s, part_id = %s
                WHERE robot_id = %s AND ticket_id = %s
            """
            update_data = (condition, repair_location, technician, part_id, robot_id, ticket_id)

            try:
                result = execute_query(update_query, update_data)
                return result
            except Exception as e:
                return f"Error updating record: {str(e)}"
        else:
            return "Record with the same robot_id and ticket_id already exists with the same condition. No update needed."

    else:
        # If no record exists, insert a new one
        insert_query = """
            INSERT INTO Repairs (robot_id, condition_type, repair_location, technician, part_id, ticket_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        insert_data = (robot_id, condition, repair_location, technician, part_id, ticket_id)

        try:
            result = execute_query(insert_query, insert_data)
            return result
        except Exception as e:
            return f"Error inserting new record: {str(e)}"
        
# @app.route('/view_orders')
# def view_orders():
#     # Retrieve orders from the database
#     connection = mysql.connector.connect(**db_config)
#     cursor = connection.cursor(dictionary=True)

#     cursor.execute("""
#     SELECT 
#     c.customer_id,
#     c.customer_name,
#     c.customer_address,
#     c.customer_email,
#     r.robot_id,
#     o.order_id
#         FROM customers c
#         LEFT JOIN orders o ON c.order_id = o.order_id
#         LEFT JOIN robots r ON o.robot_id = r.robot_id;
# """)
#     orders = cursor.fetchall()
#     return render_template('orders.html', orders=orders)

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
