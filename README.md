# AssetFlow – Asset Management System

AssetFlow is a web-based Asset Management System developed using Python, Flask, SQLite, HTML, CSS and JavaScript.

The application helps organisations manage their assets, monitor bookings, handle maintenance requests and organise department-wise asset audits through a centralised dashboard.

## Features

### 1. Dashboard
- Centralised dashboard for navigating different modules.
- Overview of the organisation's assets.

### 2. Asset Management
- Add and manage assets.
- Store asset details and categories.
- Track asset allocation and status.

### 3. Booking Management
- Manage resource booking requests.
- Track booking dates and time slots.
- Monitor booking status.

### 4. Maintenance Management
- Submit maintenance requests.
- Record asset-related issues.
- Track maintenance priority and status.

### 5. Audit Management
- Schedule department-wise audits.
- Assign auditors and audit dates.
- Edit and delete audit records.
- Designed to support physical asset verification and audit reporting.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web framework |
| SQLite | Database |
| HTML | Page structure |
| CSS | Styling and layout |
| JavaScript | Frontend interactions |
| Bootstrap | Responsive components and modals |

## Project Structure

```text
Asset-flow/
│
├── backend/
│   ├── app.py
│   ├── database.py
│   ├── init_db.py
│   ├── schema.sql
│   ├── templates/
│   └── static/
│
├── .gitignore
└── README.md
```

## Installation and Setup

1. Clone the repository:

```bash
git clone YOUR_REPOSITORY_URL
```

2. Navigate to the project:

```bash
cd Asset-flow/backend
```

3. Create and activate a virtual environment:

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Initialise the database using the project's database initialization script and schema.

6. Run the Flask application:

```bash
python app.py
```

7. Open the local URL displayed in the terminal, usually:

```text
http://127.0.0.1:5000/
```

## Learning Outcomes

Through this project, I gained practical experience in:

- Flask application development and routing.
- Database design and SQLite operations.
- CRUD operations.
- Connecting frontend forms with backend routes.
- SQL queries, joins and subqueries.
- HTML, CSS and JavaScript integration.
- Responsive web design.
- Managing application data through a relational database.

## Future Improvements

- Complete and test the asset verification workflow.
- Improve audit reporting and discrepancy tracking.
- Add user authentication and role-based access.
- Enhance dashboard analytics and visualisations.

---

**Developed as a practical full-stack development project.**