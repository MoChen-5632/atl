from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from datetime import date, datetime, timedelta
import mysql.connector
import mysql.connector.pooling
import connect



app = Flask(__name__)

dbconn = None
connection_pool = mysql.connector.pooling.MySQLConnectionPool(pool_name="atl",user=connect.dbuser, \
    password=connect.dbpass, host=connect.dbhost, \
    database=connect.dbname, autocommit=True)
connection = None

def getCursor():
    global dbconn
    global connection
    if connection is None:
        connection = connection_pool.get_connection()
    if dbconn is None:
        dbconn = connection.cursor(dictionary= True)
    return dbconn


 
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/tours", methods=["GET","POST"])
def tours():
    cursor = getCursor()
    if request.method=="GET":
        # Lists the tours        
        qstr = "select tourid, tourname from tours;" 
        cursor.execute(qstr)        
        
        tours = cursor.fetchall()    
        return render_template("tours.html", tours=tours)
    else:
        
        tourid = request.form.get("tourid")      
        qstr = "select tourgroupid, startdate from tourgroups where tourid=%s;" 
        cursor.execute(qstr,(tourid,))        
        tourgroups = cursor.fetchall()  
        return render_template("tours.html", tourid=tourid, tourgroups=tourgroups)

@app.route("/tours/list", methods=["POST"])
def tourlist():
    tourid = request.form.get('tourid')
    tourgroupid = request.form.get('tourgroupid')
    # Display the list of customers on a tour
    tourname = ""; # update to get the name of the tour
    customerlist = {} # update to get a list of customers on the tour
    return render_template("tourlist.html", tourname = tourname, customerlist = customerlist)


@app.route("/customers")
def customers():
    #List customer details.
    return render_template("customers.html")  



# Set a secret key for flash messages ?
app.secret_key = 'your_secret_key_here'  # Replace with a secure secret key!

@app.route("/booking/add", methods=["GET", "POST"])
def makebooking():
    cursor = getCursor()  # Get database cursor
    
    if request.method == "POST":
        # Handle the form submission for making a booking
        customer_id = request.form.get('customer_id')
        tour_id = request.form.get('tour_id')
        tourgroup_id = request.form.get('tourgroup_id')
        
        # Get the customer's age from the database to check age restrictions
        cursor.execute("SELECT dob FROM customers WHERE customerid = %s", (customer_id,))
        customer = cursor.fetchone()
        
        if customer:
            # Assuming calculate_age() is defined elsewhere in your app
            age = calculate_age(customer['dob'])
            
            cursor.execute("SELECT agerestriction FROM tours WHERE tourid = %s", (tour_id,))
            tour = cursor.fetchone()
            
            if tour:
                if age < tour['agerestriction']:
                    # Age restriction not met, display an error message
                    flash("Age restriction not met for this tour", "error")
                    return render_template('addbooking.html')
                
                # Insert the booking into the database
                cursor.execute("""
                    INSERT INTO tourbookings (tourgroupid, customerid) 
                    VALUES (%s, %s)
                """, (tourgroup_id, customer_id))
                cursor.connection.commit()
                
                flash("Booking successfully added!", "success")
                return redirect(url_for('makebooking'))  # Redirect to the same page

    # If GET request, show the form to add a booking
    cursor.execute("SELECT tourid, tourname FROM tours")
    tours = cursor.fetchall()
    
    # Get all customers to populate the "select customer" dropdown
    cursor.execute("SELECT customerid, CONCAT(firstname, ' ', familyname) AS fullname FROM customers")
    customers = cursor.fetchall()

    return render_template('addbooking.html', tours=tours, customers=customers)




@app.route("/customersearch", methods=["GET", "POST"])
def customersearch():
    cursor = getCursor()  # Get database cursor
    
    if request.method == "POST":
        # Get the search term from the form (both first and family name)
        search_term = request.form.get("search_term")

        # Check if the search term is provided and not empty
        if search_term:
            search_term = search_term.lower()  # Safely convert to lowercase
            qstr = """
                SELECT customerid, firstname, familyname, email, phone
                FROM customers
                WHERE LOWER(firstname) LIKE %s OR LOWER(familyname) LIKE %s;
            """
            
            search_term_wildcard = f"%{search_term}%"
            
            cursor.execute(qstr, (search_term_wildcard, search_term_wildcard))
            customers = cursor.fetchall()  # Fetch matching customers
            
            return render_template("customersearch.html", customers=customers)
        else:
            # If no search term is provided, display a message
            return render_template("customersearch.html", error="Please enter a search term.")
    
    return render_template("customersearch.html", customers=None)

