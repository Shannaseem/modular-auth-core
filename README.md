
# 🚀 modular-auth-core

**A pluggable, production-ready authentication module** built with 🧠 FastAPI — featuring multi-role support, OTP verification, secure file uploads, and dynamic templates.

> Built with ❤️ by [Abdulrehman Gulfaraz](https://github.com/abdulrehmangulfaraz) — CS Undergrad @ UET Lahore (KSK) | Backend Dev | Pentester

---

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-⚡-green.svg)
![DB](https://img.shields.io/badge/Database-PostgreSQL%20%7C%20SQLite-blue.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)

---

## 🧩 Features

- ✅ **Multi-role support** — `student`, `tutor`, `admin` (easily extendable)
- 🔐 **OTP-based Email Verification** — with expiry & resend options
- 📁 **Secure File Uploads** — CNICs, CVs, proofs (with sanitization)
- 💌 **Responsive Templates** — login, dashboards, role-based views
- 🧠 **Modular Integration** — drop-in FastAPI router (`auth_router`)
- 🔄 **DB Support** — works with both PostgreSQL and SQLite

---

## 🗂 Project Structure

```
modular-auth-core/
├── backend/
│   ├── main.py            # FastAPI entry point
│   ├── database.py        # SQLAlchemy session & engine
│   ├── models.py          # User schemas
│   ├── init_db.py         # DB seeder
│
├── frontend/
│   └── templates/         # Jinja2 HTML Forms
│       ├── base.html
│       ├── login.html
│       ├── student.html
│       ├── tutor_dashboard.html
│       └── admin.html
│
├── Requirements.txt
└── README.md
```

---

## ⚙️ Quickstart

### 📥 1. Clone & Setup

```bash
git clone https://github.com/abdulrehmangulfaraz/modular-auth-core
cd modular-auth-core
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate
pip install -r Requirements.txt
```

### ⚙️ 2. Environment Configuration
Create a `.env` file:
```ini
DATABASE_URL=sqlite:///./auth.db
OTP_EXPIRY_MINUTES=5
USER_ROLES=student,tutor,admin
```

### 🗃️ 3. Initialize Database
```bash
python backend/init_db.py
```

### 🚀 4. Launch Server
```bash
uvicorn backend.main:app --reload
```
Visit: `http://localhost:8000`

---

## 🧠 Customization Guide

### 🔄 Add/Change Roles
In `config.py` or directly in `models.py`:
```python
USER_TYPES = {
  "student": {"fields": ["email", "cnic"]},
  "tutor": {"fields": ["cv_upload", "qualification"]},
  "admin": {"fields": []}
}
```

### 🧱 Add Custom Fields
In `models.py`:
```python
class User(Base):
    profile_picture = Column(String)
    degree_title = Column(String)
```

### 🛠 Switch to PostgreSQL
Update `.env`:
```ini
DATABASE_URL=postgresql://user:pass@localhost:5432/auth_db
```

---

## 🔒 Security Highlights

- `bcrypt`-based password hashing
- OTP stored with expiry & resend protection
- Upload folder validation & file type filtering
- Minimal external dependencies

---

## 💡 Built With

| Layer       | Stack            |
|-------------|------------------|
| Framework   | FastAPI          |
| ORM         | SQLAlchemy       |
| Database    | PostgreSQL / SQLite |
| Templates   | Jinja2           |
| Mailer      | aiosmtplib (SMTP) |

---

## 🧠 Author & Maintainer

> Developed by **Abdulrehman Gulfaraz**  
> CS Undergraduate – UET Lahore (KSK)  
> 🧠 Python | FastAPI | MASM | C++ | SQL | Web Systems

🔗 GitHub: [@abdulrehmangulfaraz](https://github.com/abdulrehmangulfaraz)

---

## 📘 License

MIT — use freely, modify boldly, and give credits where due 💖
