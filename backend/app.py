from flask import Flask, redirect, request,render_template,url_for, flash
from datetime import date, datetime, timedelta
import sqlite3
from database import get_connection


app = Flask(__name__)
app.secret_key = "your_secret_key"

@app.route("/")
def home():
     return render_template("landing.html")
 
@app.route("/login")
def login_page():

    return render_template("login.html")

@app.route("/login", methods=["POST"])
def login():
    email = request.form["email"]
    password = request.form["password"]

    conn = get_connection()# connects python to database opens the restro
    cursor = conn.cursor() #executes sql we give waiter order
 
    cursor.execute(  #we get the order
        "SELECT * FROM Users WHERE Email=? AND Password=?", #select selects and * means select evrything FROM USERS TABLE 
        (email, password) #whole line means show me eveything from users table where email and password matches with the ones enetered by usewr
    )
   
    user = cursor.fetchone()#the first matching line is sent to python
   
    conn.close() #closes database connectiopn

    if user: #if there is a matrching email and paswrd from user table opn dshbrd otherwise invalid 
        return render_template("dashboard.html")
    else:
        flash("Invalid Email or Password", "danger")
        return redirect(url_for("login_page"))

@app.route("/signup")
def signup_page():
    return render_template("signup.html")
    
@app.route("/signup", methods=["POST"])
def signup():

    email = request.form["email"]
    password = request.form["password"]

    conn = get_connection() #open database
    cursor = conn.cursor()#to write 

    cursor.execute(
        "INSERT INTO Users (Email, Password) VALUES (?, ?)",
        (email, password)  #adding a new user
    )
    
    existing_user = cursor.fetchone()

    if existing_user:
        flash("Email already registered. Please log in.", "danger")
        return redirect(url_for("signup_page"))

    conn.commit()#storing the value
    conn.close()
    
    flash("Registration successful! Please log in to continue.", "success")

    return redirect(url_for("login_page"))
@app.route("/dashboard")
def dashboard():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""SELECT COUNT(*) AS total_assets
        FROM Assets""")
    total_assets = cursor.fetchone()["total_assets"]
    return render_template("dashboard.html", total_assets=total_assets)
    conn.close()

@app.route("/add_asset", methods=["POST"])
def add_asset():

    asset = request.form["assetName"]
    category = request.form["assetCategory"]
    status = request.form["assetStatus"]
    allocated = request.form["allocatedTo"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Assets
        (AssetName,Category,Status,AllocatedTo)
        VALUES(?,?,?,?)
    """,(asset,category,status,allocated))

    conn.commit()
    conn.close()

    return redirect(url_for("assets")) #when redirectig wite the function name not the html file name

@app.route("/assets")
def assets():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Assets")

    assets = cursor.fetchall()

    conn.close()

    return render_template("asset.html", assets=assets)
@app.route("/delete_asset/<int:asset_id>")
def delete_asset(asset_id):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM Assets WHERE AssetID=?", (asset_id,))#IT MEANSif  /delete_asset/1 is called then delete the asset with assetID 1 from the database
        #then we save asset_id in the asset_id variable and use it in the sql query to delete the asset with that ID from the database
        conn.commit()
        conn.close()
        return redirect(url_for("assets"))
@app.route("/get_asset/<int:asset_id>")
def get_asset(asset_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM Assets WHERE AssetID = ?",
        (asset_id,)
    )

    asset = cursor.fetchone()

    conn.close()

    return {
        "id": asset[0],
        "name": asset[1],
        "category": asset[2],
        "status": asset[3],
        "allocated": asset[4]
    }
@app.route("/update_asset/<int:asset_id>", methods=["POST"])
def update_asset(asset_id):

    asset = request.form["assetName"]
    category = request.form["assetCategory"]
    status = request.form["assetStatus"]
    allocated = request.form["allocatedTo"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE Assets
        SET AssetName = ?,
            Category = ?,
            Status = ?,
            AllocatedTo = ?
        WHERE AssetID = ?
    """, (asset, category, status, allocated, asset_id))

    conn.commit()
    conn.close()

    return redirect(url_for("assets"))

@app.route("/booking")
def bookings():
    conn = get_connection()
    cursor = conn.cursor()

    # Checking the actual columns in the Bookings table
    cursor.execute("PRAGMA table_info(Bookings)")
    columns = cursor.fetchall()

    for column in columns:
        print(column["name"])

    # Getting the selected date from the URL
    selected_date = request.args.get(#storing the date selected by user in the variable selected_date request.args.get gets the value of the parameter date from the url and if it is not present then it will return None
        "date",
        date.today().isoformat()
         #date is the parameter name in the url and date.today().isoformat() returns the current date in the format YYYY-MM-DD which is the default format of the date input field in html
    )

    # Fetching bookings for the selected date
    cursor.execute(
        "SELECT * FROM Bookings WHERE BookingDate = ?",
        (selected_date,)
    )

    selected_date_obj = datetime.strptime(
        selected_date, "%Y-%m-%d"
    ).date()

    today = date.today().isoformat()

    bookings = cursor.fetchall()

    # Calculating booking positions for the timeline
    booking_positions = {}

    for booking in bookings: # going thrg all the rows in the table of bookings
        start_hour, start_minute = map(int, booking[4].split(':'))# in the current row we are taKING column 4 which is booking time and we split it when : appears into 2 strings and to convert these into int we write int , these are stored in start_hour and start_minute
        end_hour, end_minute = map(int, booking[5].split(':'))#similar to above
        start_minutes = start_hour * 60 + start_minute#converting the time into minutes so that we can calculate the left and width of the booking in the timeline
        end_minutes = end_hour * 60 + end_minute

        left = ((start_minutes - 540) / 300) * 100# our timeline starts at 9 am which is 540 minutes from midnight and ends at 3 pm which is 900 minutes from midnight so the total time is 360 minutes and we calculate the left position of the booking in the timeline by subtracting 540 from the start time and dividing it by 360 and multiplying it by 100 to get the percentage and from this percentage of the timeline it will appear
        width = ((end_minutes - start_minutes) / 300) * 100#similar to above we calculate the width of the booking in the timeline by subtracting the start time from the end time and dividing it by 360 and multiplying it by 100 to get the percentage and from this percentage of the timeline it will appear

        booking_positions[booking[0]] = {
            "left": left,
            "width": width
        }
         #Here, booking[0] is the booking ID.
        #Suppose booking ID 1 starts atbooking_positions = {
        #1: {"left": 50.0, "width": 16.6667},
        #2: {"left": 83.3333, "width": 16.6667}
        #} 12 PM and ends at 1 PM.
    conn.close()

    return render_template(
        "booking.html",
        bookings=bookings,
        booking_positions=booking_positions,
        selected_date=selected_date,
        selected_date_obj=selected_date_obj,
        today=today,
        timedelta=timedelta
    )#passing the bookings and booking_positions to the template so that we can use them in the template to display the bookings in the timeline

@app.route("/add_booking", methods=["POST"])
def add_booking():
    employee = request.form["bookingEmployee"]
    resource = request.form["bookingResource"]
    booking_date = request.form["bookingDate"]
    start_time = request.form["startTime"]
    end_time = request.form["endTime"]
    status = request.form["bookingStatus"]

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Bookings
            (Employee, Resource, Bookingdate, StartTime, EndTime, Status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (employee, resource, booking_date,
              start_time, end_time, status))

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

    return redirect(url_for("bookings"))


@app.route("/add_department", methods=["POST"])
def add_department():

    name=request.form["deptName"]
    parent=request.form["deptParent"]
    head=request.form["deptHead"]
    status=request.form["deptStatus"]

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""
    INSERT INTO Departments
    (DepartmentName,ParentDepartment,DepartmentHead,Status)
    VALUES(?,?,?,?)
    """,(name,parent,head,status))

    conn.commit()
    conn.close()

    return "Department Added Successfully"

@app.route("/add_category", methods=["POST"])
def add_category():

    name=request.form["catName"]
    warranty=request.form["catWarranty"]
    description=request.form["catDescription"]
    status=request.form["catStatus"]

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""
    INSERT INTO Categories
    (CategoryName,Warranty,Description,Status)
    VALUES(?,?,?,?)
    """,(name,warranty,description,status))

    conn.commit()
    conn.close()

    return "Category Added Successfully"
@app.route("/add_employee", methods=["POST"])
def add_employee():

    name=request.form["empName"]
    email=request.form["empEmail"]
    department=request.form["empDepartment"]
    role=request.form["empRole"]
    status=request.form["empStatus"]

    conn=get_connection()
    cursor=conn.cursor()

    cursor.execute("""
    INSERT INTO Employees
    (Name,Email,Department,Role,Status)
    VALUES(?,?,?,?,?)
    """,(name,email,department,role,status))

    conn.commit()
    conn.close()

    return "Employee Added Successfully"

@app.route("/maintenance")
def maintenance():
    conn = get_connection()
    cursor = conn.cursor()

    # Fetch assets for the dropdown
    cursor.execute("SELECT AssetID, AssetName FROM Assets")
    assets = cursor.fetchall()

    # Fetch maintenance requests with asset names
    cursor.execute("""
        SELECT
            Maintenance.RequestID,
            Assets.AssetName,
            Maintenance.Description,
            Maintenance.RequestedBy,
            Maintenance.Priority,
            Maintenance.Status
        FROM Maintenance
        JOIN Assets
        ON Maintenance.AssetID = Assets.AssetID
    """)

    requests = cursor.fetchall()

    conn.close()

    return render_template(
        "maintenance.html",
        assets=assets,
        requests=requests
    )

    return render_template("maintenance.html")
@app.route("/add_maintenance", methods=["POST"])
def add_maintenance():
    asset_id= request.form["asset_id"]
    description = request.form["description"]
    requestedDate = date.today().isoformat()
    requested_by = request.form["requested_by"]
    priority= request.form["priority"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO Maintenance
        (Assetid, Description, RequestedDate, RequestedBy, priority)
        VALUES (?, ?, ?, ?, ?)
    """, (asset_id, description, requestedDate, requested_by, priority))

    conn.commit()
    conn.close()

    return redirect(url_for("maintenance"))

@app.route("/edit_maintenance/<int:request_id>", methods=["POST"])
def edit_maintenance(request_id):

    # Get the updated status from the form
    status = request.form["status"]

    # Validate the status
    allowed_statuses = ["Pending", "In Progress", "Completed"]

    if status not in allowed_statuses:
        return redirect(url_for("maintenance"))

    # Connect to database
    conn = get_connection()

    try:
        cursor = conn.cursor()

        # Update the maintenance request
        cursor.execute("""
            UPDATE Maintenance
            SET Status = ?
            WHERE RequestID = ?
        """, (status, request_id))

        # Save changes
        conn.commit()

    finally:
        conn.close()

    # Return to maintenance page
    return redirect(url_for("maintenance"))

# AUDIT MANAGEMENT

@app.route("/audit")
def audit():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM Audit
        ORDER BY AuditDate DESC
    """)

    audits = cursor.fetchall()
    conn.close()

    return render_template("audit.html", audits=audits)


@app.route("/add_audit", methods=["POST"])
def add_audit():
    department = request.form["department"]
    auditor = request.form["auditor"]
    audit_date = request.form["auditDate"]
    status = request.form["status"]
    discrepancy = request.form["discrepancy"]

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO Audit
            (Department, Auditor, AuditDate, Status, Discrepancy)
            VALUES (?, ?, ?, ?, ?)
        """, (department, auditor, audit_date, status, discrepancy))

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

    return redirect(url_for("audit"))


@app.route("/edit_audit/<int:audit_id>", methods=["POST"])
def edit_audit(audit_id):
    department = request.form["department"]
    auditor = request.form["auditor"]
    audit_date = request.form["auditDate"]
    status = request.form["status"]
    discrepancy = request.form["discrepancy"]

    allowed_statuses = ["Scheduled", "In Progress", "Completed"]

    if status not in allowed_statuses:
        return redirect(url_for("audit"))

    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE Audit
            SET Department = ?,
                Auditor = ?,
                AuditDate = ?,
                Status = ?,
                Discrepancy = ?
            WHERE AuditID = ?
        """, (
            department,
            auditor,
            audit_date,
            status,
            discrepancy,
            audit_id
        ))

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

    return redirect(url_for("audit"))


@app.route("/delete_audit/<int:audit_id>", methods=["POST"])
def delete_audit(audit_id):
    conn = get_connection()

    try:
        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM Audit
            WHERE AuditID = ?
        """, (audit_id,))

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

    return redirect(url_for("audit"))
@app.route("/audit_assets/<int:audit_id>")
def audit_assets(audit_id):
    conn = get_connection()
    cursor = conn.cursor()

    # Get the selected audit
    cursor.execute("""
        SELECT * FROM Audit
        WHERE AuditID = ?
    """, (audit_id,))

    audit = cursor.fetchone()

    if audit is None:
        conn.close()
        return redirect(url_for("audit"))

    # Get assets belonging to the audit department
    cursor.execute("""
        SELECT AssetID, AssetName, Category, Status, AllocatedTo
        FROM Assets
        WHERE AllocatedTo IN (
            SELECT Name FROM Employees
            WHERE Department = ?
        )
    """, (audit["Department"],))

    assets = cursor.fetchall()

    conn.close()

    return render_template(
        "audit_assets.html",
        audit=audit,
        assets=assets
    )
@app.route("/save_audit/<int:audit_id>", methods=["POST"])
def save_audit(audit_id):

    conn = get_connection()

    try:
        cursor = conn.cursor()

        # Get all submitted asset verification details
        asset_ids = request.form.getlist("asset_id")
        statuses = request.form.getlist("verification_status")
        remarks = request.form.getlist("remarks")

        # Save each asset's verification result
        for asset_id, status, remark in zip(asset_ids, statuses, remarks):

            cursor.execute("""
                INSERT INTO AuditDetails
                (AuditID, AssetID, VerificationStatus, Remarks)
                VALUES (?, ?, ?, ?)
            """, (audit_id, asset_id, status, remark))

        # Mark audit as completed
        cursor.execute("""
            UPDATE Audit
            SET Status = 'Completed'
            WHERE AuditID = ?
        """, (audit_id,))

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        conn.close()

    return redirect(url_for("audit"))

@app.route("/logout")
def logout():
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)