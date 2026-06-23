# 🩺 Donora – Organ Donation Platform

## 🧩 Overview

Donora is a non-profit web-based organ donation platform developed using Python (Django) that connects living organ donors and recipients through a compatibility-based matching system.

The platform supports organ donation requests for kidney, liver, lung, and skin transplants. It uses donor and recipient information, including blood group and organ compatibility, to identify suitable matches and generate a unique transplantation ID for each successful donor–recipient pair.

The system provides donor and recipient registration, secure document uploads, cancellation and re-application workflows, notification management, acknowledgment generation, and transplantation tracking functionalities.

The platform includes two administrative components:

1. Django Admin Panel for managing users, donor and recipient records, matches, notifications, and platform operations.

2. A dedicated Hospital Single Page Application (SPA) that allows hospital staff to view donor, recipient, and transplantation records, apply custom date-range filters, and export records in CSV and PDF formats for operational tracking and documentation.

---

## ✨ Features

* Donor registration system
* Recipient registration system
* Blood group and organ compatibility matching
* Unique transplantation ID generation
* Automated donor–recipient matching workflow
* Organ-specific donor and recipient applications
* Cancellation and re-application functionality
* User authentication and account management
* Notification management system
* Secure document upload support
* Contact submission management
* Profile management functionality
* Password management functionality
* Acknowledgment generation for successful matches
* Database-driven workflow automation
* Django Admin Panel for platform administration
* Dedicated Hospital SPA for transplantation management
* Date-range filtering for donor, recipient, and match records
* CSV export functionality for hospital records
* PDF export functionality for hospital records
* Transplantation monitoring and record management tools
* Responsive user interface

---

## 🛠️ Technologies Used

### Backend

* Python
* Django

### Frontend

* HTML5
* CSS3
* JavaScript

### Database

* MySQL

### Libraries & Packages

* mysqlclient
* Pillow
* python-dotenv
* ReportLab

---

## 📂 Project Structure

```plaintext
Donora/
│
├── adminspa/
│   ├── static/
│   ├── templates/
│   │   └── adminspa/
│   │       └── index.html
│   ├── urls.py
│   ├── views.py
│   └── apps.py
│
├── core/
│   ├── migrations/
│   ├── templates/
│   │   ├── homepage.html
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── donor_form.html
│   │   ├── recipient_form.html
│   │   ├── dashboard.html
│   │   ├── notifications.html
│   │   ├── acknowledgment.html
│   │   ├── aboutus.html
│   │   ├── contactus.html
│   │   ├── kidney.html
│   │   ├── liver.html
│   │   ├── lung.html
│   │   ├── skin.html
│   │   ├── organ.html
│   │   └── additional policy pages
│   │
│   ├── forms.py
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── context_processors.py
│   └── admin.py
│
├── Donora/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── media/
├── static/
├── static_src/
├── venv/
│
├── .env
├── manage.py
├── requirements.txt
├── README.md
└── db.sqlite3
```

---

## 🚀 How to Run the Project

### Clone the Repository

```bash
git clone https://github.com/ArshyaBhagat/Donora.git
cd Donora
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Virtual Environment

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```env
SECRET_KEY=your_secret_key
DB_PASSWORD=your_database_password
```

### Apply Migrations

```bash
python manage.py migrate
```

### Run the Application

```bash
python manage.py runserver
```

---

## 🔐 Security

Sensitive configuration values are stored using environment variables and excluded from version control.

Examples:

* `.env`
* database credentials
* uploaded documents
* local environment files

The platform includes authenticated user access, protected document handling, and secure database-driven workflows.

---

## 👩‍💻 Developer

**Arshya Bhagat**

Designed and developed the complete Donora platform, including backend development, database design, donor–recipient matching logic, user workflows, document management, notification handling, and frontend integration using Django, MySQL, HTML, CSS, and JavaScript.

Implemented the Django Admin Panel for platform administration and developed a dedicated Hospital Single Page Application (SPA) for transplantation management, enabling hospital staff to view donor, recipient, and matched transplantation records, apply date-based filters, and export data in CSV and PDF formats.

Developed as an academic project at M.E.S. Garware College of Commerce (Autonomous), Pune.

---

## ❤️ Vision

To leverage technology for simplifying organ donor and recipient matching while promoting awareness, accessibility, and social impact through a structured and efficient organ donation platform.
