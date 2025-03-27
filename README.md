# FreshCart Application

## Project Name: FreshCart
---

## Description
The FreshCart Application is a web-based platform developed using Flask, Celery, and Vue CLI. It facilitates product management, monthly report generation, daily reminders, and data export to CSV files. It is designed with a user-friendly interface and supports role-based access control.

## Technologies Used
- **Flask** - Python web framework for backend development
- **Celery** - Asynchronous task queue/job queue system
- **Vue CLI** - Command-line interface for Vue.js development
- **CSS** - For frontend styling
- **Flask-Security** - Security-related extensions for user authentication
- **Flask-CORS** - Handling Cross-Origin Resource Sharing
- **Redis** - Message broker and result backend for Celery
- **SQLite** - Lightweight database for data storage

## Features
- User authentication and role-based access control
- Background tasks (reminders, report generation) using Celery
- Product category and request management
- Shopping cart and purchase functionality
- Exporting product data to CSV files
- Automated reminders for inactive users
- Monthly progress reports

## Architecture
FreshCart follows the **Model-View-Controller (MVC)** architecture:
- **Model:** Defines database schema using SQLAlchemy models
- **View:** Frontend built using Vue CLI for a dynamic user experience
- **Controller:** Flask handles backend logic, API routes, and Celery tasks for background processing

## Database Schema
1. **User:** Stores user details like email, username, password, and roles.
2. **Role:** Defines user roles and access levels.
3. **Request:** Stores user requests for approvals.
4. **Category:** Manages product categories and their relationships.
5. **Category Requests:** Handles category creation requests.
6. **Category Update Request:** Manages category update requests.
7. **Category Delete Request:** Handles category deletion requests.
8. **Product:** Stores product details like name, expiry date, price, and stock.
9. **Cart:** Stores user-specific shopping cart details.
10. **BoughtProducts:** Maintains records of purchased products.

## API Design
- User and manager sign-up/login.
- Category management (add, modify, delete, request approvals).
- Product management (add, modify, delete, purchase).
- Cart operations (add to cart, remove from cart, checkout).
- User dashboard with role-based access control.
- Yaml configuration file available in the `Backend` folder.

## Installation & Setup

### Prerequisites
Ensure you have the following installed:
- **WSL (Windows Subsystem for Linux)**

### Installation Steps
1. **Clone the repository** and download the project.
2. **Add the `node_modules` folder** inside the `freshcart` directory.
3. **Open a WSL terminal** and run:
   ```bash
   wsl
   ```
4. Navigate to the Backend directory and activate the virtual environment:
   ```bash
   cd Backend
   source venv/bin/activate
   ```
5. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Project
Open **6 terminals** and execute the following commands:

#### **Terminal 1: Frontend**
```bash
cd frontend
npm run serve
```

#### **Terminal 2: Backend**
```bash
cd Backend
source venv/bin/activate
python app.py
```

#### **Terminal 3: Redis Server**
```bash
source myenv/bin/activate
redis-server
```
To stop Redis:
```bash
sudo service redis-server stop
sudo lsof -i :6379
sudo kill -9 PID
```

#### **Terminal 4: Celery Worker**
```bash
source myenv/bin/activate
celery -A app.celery worker -l info
```

#### **Terminal 5: Celery Beat**
```bash
source myenv/bin/activate
celery -A app.celery beat --max-interval 2 -l info
```

#### **Terminal 6: MailHog**
MailHog is required for handling emails. Run:
```bash
~/go/bin/MailHog
```

## Additional Information
- **FreshCart can send emails and daily reminders via GSpace.**
- **Built with Vue CLI, making it easy to install and run.**

## Video Demonstration
Watch the demo video here: [Click Here](https://drive.google.com/file/d/1XMJzLhbjcCL9-WtGkYSLHtOEiCdSIf65/view?usp=drive_link)


