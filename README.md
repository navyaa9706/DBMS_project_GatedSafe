# GatedSafe – Security Management System

## 📌 Overview
**GatedSafe** is a DBMS + Flask based project designed to manage security in gated communities or organizations. It provides a structured way to handle **user authentication, role-based access control, and activity logging**. The system ensures that only authorized individuals can access specific areas or resources, while administrators can monitor and manage permissions effectively.


## ⚙️ Tech Stack
- **Backend:** Python (Flask Framework)  
- **Database:** MySQL / PostgreSQL (Relational DBMS concepts applied)  
- **Frontend:** HTML, CSS, Jinja2 templates
 

## 🚀 Features
- 🔒 **User Authentication** – Secure login with hashed passwords  
- 🛂 **Role-Based Access Control (RBAC)** – Different permissions for guards, residents, and admins  
- 📜 **Activity Logs** – Track entries, exits, and user actions  
- 🖥️ **Admin Dashboard** – Manage users, roles, and permissions  
- 📊 **Database Integration** – Normalized schema with constraints and relationships  


## 🛠️ Installation & Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/navyaa9706/DBMS_project_GatedSafe.git
   cd DBMS_project_GatedSafe
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure your database connection in `config.py`.  
4. Run the Flask app:
   ```bash
   flask run
   ```
5. Open `http://127.0.0.1:5000/` in your browser.


## 📄 Database Schema
- **Users Table:** Stores user details and hashed passwords  
- **Roles Table:** Defines roles (Admin, Guard, Resident)  
- **Permissions Table:** Maps roles to allowed actions  
- **Logs Table:** Records activity for auditing  


## 🤝 Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you’d like to change.

👉 This README will make your repo look professional and easy to understand.  
Would you like me to also **add a sample ER diagram** (Entity-Relationship diagram) section so that your DBMS design is visually clear to visitors?
