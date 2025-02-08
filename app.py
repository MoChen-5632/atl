from flask import Flask, flash
from flask import render_template
from flask import request
from flask import redirect
from flask import url_for
from datetime import date, datetime, timedelta
import mysql.connector
import mysql.connector.pooling
import connect



app = Flask(__name__)
app.secret_key = '/~76UgF&b8.`5f(!B8H3'

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


@app.route("/customers")
def customers():
    #List customer details.
    connection = getCursor()
    connection.execute("SELECT * FROM customers;")
    Customerlist = connection.fetchall()

    return render_template("customers.html", customerlist = Customerlist)


@app.route("/tours/list", methods=["GET", "POST"])
def tourlist():
    connection = getCursor()
    # Fetch all tour groups across all tours
    connection.execute("""
        SELECT tourgroups.tourgroupid, tourgroups.startdate, tours.tourname
        FROM tourgroups
        JOIN tours ON tourgroups.tourid = tours.tourid
        ORDER BY tours.tourname, tourgroups.startdate;
    """)
    tourgroups = connection.fetchall()


    customers = []
    tourname = None
    startdate = None

    if request.method == "POST":
        tourgroup_id = request.form.get("tourgroup")

        if tourgroup_id:
            # Fetch tour name and start date for the selected tourgroup
            connection.execute("""
                SELECT tours.tourname, tourgroups.startdate
                FROM tourgroups
                JOIN tours ON tourgroups.tourid = tours.tourid
                WHERE tourgroups.tourgroupid = %s;
            """, (tourgroup_id,))
            tour_info = connection.fetchone()      


            if tour_info:
                tourname = tour_info['tourname']
                startdate = tour_info['startdate']
                
                # Fetch customers in the selected tourgroup
                connection.execute("""
                    SELECT customers.customerid, customers.firstname, customers.familyname, customers.dob, customers.email, customers.phone
                    FROM tourbookings
                    JOIN customers ON tourbookings.customerid = customers.customerid
                    WHERE tourbookings.tourgroupid = %s
                    ORDER BY customers.familyname ASC, customers.dob DESC;
                """, (tourgroup_id,))
                customers = connection.fetchall()

    return render_template("tourlist.html",
                           tourgroups=tourgroups, 
                           tourname=tourname, 
                           startdate=startdate, 
                           customers=customers)



@app.route("/customersearch", methods=["GET", "POST"])
def customersearch():
    connection = getCursor()  
    
    if request.method == "POST":
        # Get the search term from the form 
        search_term = request.form.get("search_term")

        # Check if the search term is provided and not empty
        if search_term:
            search_term = search_term.lower()  # Safely convert to lowercase
            qstr = """
                SELECT customerid, firstname, familyname, dob, email, phone
                FROM customers
                WHERE LOWER(firstname) LIKE %s OR LOWER(familyname) LIKE %s;
            """
            
            search_term_wildcard = f"%{search_term}%"
            
            connection.execute(qstr, (search_term_wildcard, search_term_wildcard))
            customers = connection.fetchall()  # Fetch matching customers
            
            return render_template("customersearch.html", customers=customers)
        else:
            # If no search term is provided, display a message
            return render_template("customersearch.html", error="Please enter a search term.")
    
    return render_template("customersearch.html", customers=None)



@app.route("/booking/add", methods=["GET", "POST"])
def addbooking():
    connection = getCursor()
    
    if request.method == 'POST':
        # Retrieve form values from three fields: customer, tour, and tourgroup.
        customerid = request.form.get('customer')
        tourid_selected = request.form.get('tour')
        tourgroupid = request.form.get('tourgroup')
        
        # Ensure all selections were made.
        if not customerid or not tourid_selected or not tourgroupid:
            flash("Please select a customer, a tour, and a tour group.")
            return redirect(url_for('addbooking'))
            
        # 1. Retrieve the selected tourgroup and verify it exists and is in the future.
        query = "SELECT tourid, startdate FROM tourgroups WHERE tourgroupid = %s"
        connection.execute(query, (tourgroupid,))
        tourgroup = connection.fetchone()
        if not tourgroup:
            flash("Invalid tour group selected.")
            return redirect(url_for('addbooking'))
        
        if tourgroup['startdate'] <= date.today():
            flash("You can only book tour groups with a start date in the future.")
            return redirect(url_for('addbooking'))
        
        # 2. Ensure the tourgroup belongs to the tour selected.
        if int(tourid_selected) != tourgroup['tourid']:
            flash("The selected tour group does not belong to the chosen tour.")
            return redirect(url_for('addbooking'))
        
        # 3. Ensure the customer is not already booked for this tourgroup
        query = "SELECT 1 FROM tourbookings WHERE customerid = %s AND tourgroupid = %s"
        connection.execute(query, (customerid, tourgroupid))
        existing_booking = connection.fetchone()

        if existing_booking:
            flash("This customer is already booked for the selected tour group.")
            return redirect(url_for('addbooking'))
        

        # 4. Retrieve the tour’s age restriction.
        query = "SELECT agerestriction FROM tours WHERE tourid = %s"
        connection.execute(query, (tourid_selected,))
        tour = connection.fetchone()
        if not tour:
            flash("Selected tour not found.")
            return redirect(url_for('addbooking'))
        age_restriction = tour['agerestriction']

        
        
        # 5. Retrieve the customer's details (date of birth) to check their age.
        query = "SELECT dob FROM customers WHERE customerid = %s"
        connection.execute(query, (customerid,))
        customer = connection.fetchone()
        if not customer:
            flash("Selected customer not found.")
            return redirect(url_for('addbooking'))
        
        # Calculate customer's age.
        dob = customer['dob']
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        
        if age < age_restriction:
            flash(f"Booking cannot be made. This tour requires a minimum age of {age_restriction} and the customer is only {age}.")
            return redirect(url_for('addbooking'))
        
        # 6. Insert the booking into the database.
        insert_query = "INSERT INTO tourbookings (tourgroupid, customerid) VALUES (%s, %s)"
        connection.execute(insert_query, (tourgroupid, customerid))

        flash("Booking added successfully!")
        return redirect(url_for('addbooking'))
    
    else:
        # GET request: load data for the form.
        # Retrieve all customers.
        query = "SELECT customerid, firstname, familyname FROM customers ORDER BY familyname, firstname"
        connection.execute(query)
        customers = connection.fetchall()
        
        # Retrieve all tours.
        query = "SELECT tourid, tourname, agerestriction FROM tours ORDER BY tourname"
        connection.execute(query)
        tours = connection.fetchall()
        
        # Retrieve tour groups with a future start date (with associated tour details).
        query = """
            SELECT tg.tourgroupid, tg.tourid, tg.startdate, t.tourname 
            FROM tourgroups tg
            JOIN tours t ON tg.tourid = t.tourid
            WHERE tg.startdate > CURDATE()
            ORDER BY tg.startdate
        """
        connection.execute(query)
        tourgroups = connection.fetchall()
        
        return render_template('addbooking.html', customers=customers, tours=tours, tourgroups=tourgroups)




@app.route('/customer/add', methods=["GET","POST"])
def addcustomer():
    if request.method == "GET":
        return render_template("customerform.html")
    print (request.form)
    # get information from the form
    firstname = request.form.get("firstname")
    familyname = request.form.get("familyname")
    dob = request.form.get("dob")
    email = request.form.get("email")
    phone = request.form.get("phone")

    dataerror = False
    ## server side data validation
    if not firstname.isalpha():
        flash('First name must contain letters only')
        dataerror = True
    if not familyname.isalpha():
        flash('Family name must contain letters only')
        dataerror = True
    if not email or '@' not in email:
        flash('Please enter a valid email address')
        dataerror = True
    if not dob: 
        flash('Date of birth is required')
        dataerror = True
    dob_date = datetime.strptime(dob, "%Y-%m-%d").date()
    if dob_date >= datetime.today().date():
        flash('Date of birth cannot be in the future')
        dataerror = True

    # if we have a validation error return to the form
    if dataerror:
        return render_template("customerform.html")    

    connection = getCursor()

    # Insert customer data
    connection.execute("""
        INSERT INTO customers (firstname, familyname, dob, email, phone)
        VALUES (%s, %s, %s, %s, %s);
    """, (firstname, familyname, dob, email, phone))

    flash("Customer added successfully!")

    return redirect("/customers")



@app.route("/customer/edit/<int:customerid>", methods=["GET", "POST"])
def editcustomer(customerid):
    connection = getCursor()

    if request.method == "GET":
        connection.execute("SELECT * FROM customers WHERE customerid = %s;", (customerid,))
        customer = connection.fetchone()

        if not customer:
            return "Customer not found", 404

        return render_template("customeredit.html", customer=customer)

    # If form is submitted (POST request)
    firstname = request.form["firstname"]
    familyname = request.form["familyname"]
    dob = request.form["dob"]
    email = request.form["email"]
    phone = request.form["phone"]


    dataerror = False
    ## server side data validation
    if not firstname.isalpha():
        flash('First name must contain letters only')
        dataerror = True
    if not familyname.isalpha():
        flash('Family name must contain letters only')
        dataerror = True
    if not email or '@' not in email:
        flash('Please enter a valid email address')
        dataerror = True
    if not dob: 
        flash('Date of birth is required')
        dataerror = True
    dob_date = datetime.strptime(dob, "%Y-%m-%d").date()
    if dob_date >= datetime.today().date():
        flash('Date of birth cannot be in the future')
        dataerror = True

    # if we have a validation error return to the form
    if dataerror:
        return render_template("customerform.html")    
    
    connection.execute("UPDATE customers SET firstname=%s, familyname=%s, dob=%s, email=%s, phone=%s WHERE customerid=%s;",
                       (firstname, familyname, dob, email, phone, customerid))

    return redirect(url_for("customers"))



@app.route("/customer/booking/<int:customerid>")
def customerbooking(customerid):
    connection = getCursor()

    # Fetch customer details
    connection.execute("SELECT firstname, familyname FROM customers WHERE customerid = %s", (customerid,))
    customer = connection.fetchone()

    if not customer:
        flash("Customer not found!", "danger")
        return redirect(url_for("customers"))

    # Get total tour destinations booked
    connection.execute("""
        SELECT COUNT(*) AS total_destinations
        FROM tourbookings tb
        JOIN tourgroups tg ON tb.tourgroupid = tg.tourgroupid
        JOIN itineraries i ON tg.tourid = i.tourid
        WHERE tb.customerid = %s
    """, (customerid,))
    total_destinations = connection.fetchone()["total_destinations"]

    # Fetch past, current, and future bookings
    connection.execute("""
        SELECT t.tourname, tg.startdate, COUNT(i.destinationid) AS num_destinations,
            CASE 
                WHEN tg.startdate < CURDATE() THEN 'past'
                WHEN tg.startdate = CURDATE() THEN 'current'
                ELSE 'future'
            END AS booking_status
        FROM tourbookings tb
        JOIN tourgroups tg ON tb.tourgroupid = tg.tourgroupid
        JOIN tours t ON tg.tourid = t.tourid
        JOIN itineraries i ON t.tourid = i.tourid
        WHERE tb.customerid = %s
        GROUP BY t.tourname, tg.startdate, booking_status
        ORDER BY tg.startdate DESC
    """, (customerid,))


    bookings = connection.fetchall()

    # Organize bookings into categories
    past_bookings = [b for b in bookings if b["booking_status"] == "past"]
    current_bookings = [b for b in bookings if b["booking_status"] == "current"]
    future_bookings = [b for b in bookings if b["booking_status"] == "future"]

    return render_template("customerbooking.html",
                           customer=customer,
                           total_destinations=total_destinations,
                           past_bookings=past_bookings,
                           current_bookings=current_bookings,
                           future_bookings=future_bookings)
