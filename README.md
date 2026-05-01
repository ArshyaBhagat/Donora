# 🩺 Donora – Organ Donation Platform

## 🧩 Overview

Donora is a **non-profit web-based platform** developed using Python (Django) that connects living organ donors and recipients for kidney, liver, lung, and skin transplants.

It uses a **matching algorithm** based on blood group and organ compatibility, generating a unique **transplantation ID** for each donor–recipient pair.

---

## ⚙️ Tech Stack

* **Backend:** Python (Django)
* **Frontend:** HTML, CSS, JavaScript
* **Database:** MySQL

---

## 💡 Features

* 🔗 Donor–Recipient matching algorithm
* 📝 Registration, cancellation, and re-application flows
* 🆔 Unique transplantation ID system
* 🔐 Secure authentication system
* 📊 Admin dashboard for monitoring and reports
* ❤️ Free and non-profit initiative

---

## 🚀 How to Run the Project

```bash
git clone https://github.com/ArshyaBhagat/Donora.git
cd Donora
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` file:

```env
SECRET_KEY=your_secret_key_here
DB_PASSWORD=your_database_password
```

Run:

```bash
python manage.py migrate
python manage.py runserver
```

---

## 👩‍💻 Developer

**Arshya Bhagat — Full-Stack Developer**

Spearheaded the complete development of Donora, handling both backend and frontend. Designed and implemented the donor–recipient matching logic, managed database integration, and ensured seamless user experience across the platform.

Developed as part of the final-year curriculum at
*M.E.S. Garware College of Commerce (Autonomous)*.

---

## ❤️ Vision

Leveraging technology to simplify the organ donation process and promote meaningful social impact.
