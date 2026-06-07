# 🩺 Donora – Living Organ Donation Platform

## 🧩 Overview

Donora is a **non-profit web-based platform** developed using **Python (Django)** that connects living organ donors and recipients for kidney, liver, lung, and skin transplants.

The platform implements a **rule-based donor–recipient matching system** using blood group and organ compatibility. Upon successful matching, a unique **transplantation ID** is generated for each donor–recipient pair to support transplantation tracking and management.

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

---

## 💡 Features

* 🔗 Rule-based donor–recipient matching using blood group and organ compatibility
* 📝 Registration, cancellation, and re-application workflows
* 🆔 Unique transplantation ID generation for matched donor–recipient pairs
* 🔐 Secure user authentication and account management
* 🔔 Notification system for donor and recipient updates
* 📁 Secure document upload for Aadhaar and blood reports
* 📊 Administrative monitoring and transplantation management
* ❤️ Free and non-profit initiative focused on social impact

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

#### Windows

```bash
venv\Scripts\activate
```

#### Linux / macOS

```bash
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Create Environment File

Create a `.env` file in the project root directory:

```env
SECRET_KEY=your_secret_key_here
DB_PASSWORD=your_database_password
```

### Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Run Development Server

```bash
python manage.py runserver
```

Open:

```text
http://127.0.0.1:8000/
```

---

## 📂 Core Modules

* User Authentication
* Donor Registration
* Recipient Registration
* Organ Management
* Donor–Recipient Matching
* Notification Management
* Transplantation Tracking
* Re-application Management
* Contact Submission Management

---

## 👩‍💻 Developer

**Arshya Bhagat – Developer**

Responsible for the complete development of Donora, including backend development, database design, business logic implementation, frontend integration, and donor–recipient matching workflows.

Designed and implemented blood-group and organ compatibility matching, notification workflows, user management features, and transplantation tracking mechanisms.

Developed as part of the final-year curriculum at **M.E.S. Garware College of Commerce (Autonomous), Pune**.

---

## ❤️ Vision

Leveraging technology to simplify the organ donation process, improve donor–recipient connectivity, and promote meaningful social impact through accessible healthcare solutions.
