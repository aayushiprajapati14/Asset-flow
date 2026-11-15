CREATE TABLE IF NOT EXISTS Users (
    UserID INTEGER PRIMARY KEY AUTOINCREMENT,
    Email TEXT NOT NULL UNIQUE,
    Password TEXT NOT NULL
);

CREATE TABLE Assets(
    AssetID INTEGER PRIMARY KEY AUTOINCREMENT,
    AssetName TEXT,
    Category TEXT,
    Status TEXT,
    AllocatedTo TEXT
);

CREATE TABLE Departments(
    DepartmentID INTEGER PRIMARY KEY AUTOINCREMENT,
    DepartmentName TEXT,
    ParentDepartment TEXT,
    DepartmentHead TEXT,
    Status TEXT
);

CREATE TABLE Categories(
    CategoryID INTEGER PRIMARY KEY AUTOINCREMENT,
    CategoryName TEXT,
    Warranty TEXT,
    Description TEXT,
    Status TEXT
);

CREATE TABLE Employees(
    EmployeeID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT,
    Email TEXT,
    Department TEXT,
    Role TEXT,
    Status TEXT
);

CREATE TABLE Bookings(
    BookingID INTEGER PRIMARY KEY AUTOINCREMENT,
    Resource TEXT,
    BookingDate INTEGER,
    StartTime INTEGER,
    EndTime INTEGER,
    Status TEXT
);
CREATE TABLE IF NOT EXISTS Maintenance(
    RequestID INTEGER PRIMARY KEY AUTOINCREMENT,
    AssetID INTEGER,
    RequestedDate TEXT ,
    Description TEXT,
    Status TEXT default 'Pending',
    RequestedBy TEXT,
    Priority TEXT,
    Technician TEXT,
    FOREIGN KEY (AssetID) REFERENCES Assets(AssetID)
);
CREATE TABLE IF NOT EXISTS Audit (
    AuditID INTEGER PRIMARY KEY AUTOINCREMENT,
    Department TEXT NOT NULL,
    Auditor TEXT NOT NULL,
    AuditDate TEXT NOT NULL,
    Status TEXT DEFAULT 'Scheduled',
    Discrepancy TEXT
);