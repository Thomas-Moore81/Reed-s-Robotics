from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# replace these with the database stuff for whoever is doing the database
db_config = {
    'host': '',
    'user': '',
    'password': '',
    'database': ''
}

def fetch_past_repairs():
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor(dictionary=True)

        cursor.execute("SELECT * FROM repairs")
        past_repairs = cursor.fetchall()

        return past_repairs

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return []

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

@app.route('/')
def index():
    past_repairs = fetch_past_repairs()
    return render_template('orders.html', past_repairs=past_repairs)

@app.route('/submit_repair', methods=['POST'])
def submit_repair():
    robot_id = request.form['robot_id']
    condition = request.form['condition']
    repair_location = request.form['repair_location']
    technician = request.form['technician']
    part_id = request.form['part_id']

    add_repair_to_database(robot_id, condition, repair_location, technician, part_id)

    # Redirect to the home page after submitting the repair
    return redirect(url_for('order.html'))

def add_repair_to_database(robot_id, condition, repair_location, technician, part_id):
    try:
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        add_repair_query = "INSERT INTO repairs (robot_id, condition, repair_location, technician, part_id) " \
        "VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(add_repair_query, (robot_id, condition, repair_location, technician, part_id))
        connection.commit()

        print("processing...")

    except mysql.connector.Error as err:
        print(f"Error: {err}")

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    app.run(debug=True)
