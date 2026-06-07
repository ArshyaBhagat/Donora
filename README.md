# 🩺 Donora – Organ Donation Platform

## 🧩 Overview

Donora is a non-profit web-based platform developed using Python (Django) that connects living organ donors and recipients for organ transplantation.

The platform facilitates donor and recipient registration, matches compatible donors and recipients based on blood group and organ compatibility, and generates a unique transplantation ID for each successful match.

The project also includes cancellation and re-application workflows, notification management, document uploads, and an administrative dashboard for monitoring platform activities.

---

## ⚙️ Tech Stack

### Backend

* Python
* Django

### Frontend

* HTML
* CSS
* JavaScript

### Database

* MySQL

### Additional Libraries

* python-dotenv
* Pillow
* ReportLab

---

## 💡 Features

* Donor and recipient registration system
* Organ compatibility and blood group matching
* Unique transplantation ID generation
* Secure user authentication and account management
* Donor and recipient cancellation workflows
* Re-application functionality after cancellation
* Notification management system
* Contact form submission handling
* File upload support for Aadhaar documents and blood reports
* Password management and account settings
* Administrative dashboard for monitoring transplant activities

---

## 📂 Project Structure

```plaintext
Donora/
│
├── adminspa/
│   ├── static/
│   ├── templates/
│   ├── urls.py
│   └── views.py
│
├── core/
│   ├── migrations/
│   ├── templates/
│   ├── forms.py
│   ├── models.py
│   ├── urls.py
│   └── views.py
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
│
├── manage.py
├── requirements.txt
├── README.md
└── .env
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

venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Create .env File

Create a `.env` file in the project root directory:

```env
SECRET_KEY=your_secret_key_here
DB_PASSWORD=your_database_password
```

### Apply Migrations

```bash
python manage.py migrate
```

### Run the Development Server

```bash
python manage.py runserver
```

---

## 🔐 Security

Sensitive information is managed through environment variables and excluded from version control.

Examples:

* `.env`
* uploaded media files
* cache files
* virtual environment files

The application uses Django's built-in authentication system for secure user account management and access control.

---

## 👩‍💻 Developer

**Arshya Bhagat — Full-Stack Developer**

Developed both the frontend and backend of Donora as an academic project.

Responsible for designing the donor–recipient matching workflow, implementing database models, creating registration and notification systems, managing document uploads, and developing the overall user experience using Django, MySQL, HTML, CSS, and JavaScript.

Developed as part of the final-year curriculum at M.E.S. Garware College of Commerce (Autonomous), Pune.

---

## ❤️ Vision

To leverage technology for simplifying the organ donation process, improving donor–recipient connectivity, and promoting meaningful social impact through accessible healthcare-focused solutions.
