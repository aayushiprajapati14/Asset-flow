from flask import Flask, redirect, request,render_template,url_for, flash
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

    conn = get_connection()# connects [ython to database opens the restro
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
        return "Invalid Email or Password"
    
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

    return "Asset Added Successfully"

@app.route("/assets")
def assets():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM Assets")

    assets = cursor.fetchall()

    conn.close()

    return render_template("asset.html", assets=assets)
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

if __name__ == "__main__":
    app.run(debug=True)