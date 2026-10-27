# TimeSync ⏱️

A clean, minimalist academic timetable management application built with **Flask**, **SQLite**, and **Material Design 3 (M3)** with vivid emerald green accents.

Designed for colleges and schools to quickly browse daily class schedules without visual clutter, paired with a protected administrative portal for updating schedules in real time.

---

## ✨ Features

- **Material Design 3 (M3) Interface**:
  - Expressive dark surface system with fresh emerald green tonal accents (`#4ade80`).
  - M3 pill buttons, outlined text fields, and tactile filter chips.
  - Minimalist layout focused purely on schedule information—no walls of text.
- **Weekly Schedule Filtering**:
  - Responsive day-by-day tabs (Monday through Saturday).
  - Class period counters and automatic "Today" highlighting.
  - Remembers last searched branch and section across visits.
- **Admin Management Portal**:
  - Secure credential authentication with password hashing (`Werkzeug`).
  - Add, edit, or delete periods on demand per branch, section, and day.
  - Multi-admin account creation system.
- **Production Ready**:
  - Stateless filesystem session management via `Flask-Session`.
  - WSGI deployment ready with `Gunicorn`.

---

## 🛠️ Tech Stack

- **Backend**: Python 3.10+, Flask, SQLite3, Flask-Session
- **Frontend**: HTML5, Vanilla JavaScript, CSS3 (Material Design 3 tokens & layout)
- **Icons & Fonts**: Google Material Symbols & Roboto
- **Server**: Gunicorn WSGI

---

## 🚀 Getting Started

### 1. Prerequisites

- Python 3.10 or higher
- Git

### 2. Clone the Repository

```bash
git clone https://github.com/your-username/timesync.git
cd timesync
```

### 3. Create and Activate Virtual Environment

```bash
# Linux / macOS
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Environment Configuration

Create a `.env` file in the root directory:

```env
SECRET_KEY=your_secret_key_here
```

### 6. Run the Application

#### Development Server
```bash
python run.py
```
Visit `http://localhost:5000` in your browser.

#### Production Server (Gunicorn)
```bash
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

---

## 📂 Project Structure

```text
timesync/
├── app/
│   ├── __init__.py          # App package initialization
│   ├── routes.py            # Public timetable routes
│   ├── admin_routes.py      # Admin portal & schedule modifier routes
│   ├── db.py                # Timetable SQLite database helper
│   └── admin_db.py          # Admin account SQLite database helper
├── static/
│   ├── style.css            # Material Design 3 stylesheet (green accents)
│   └── timetable.js         # Tab switching, prefilling, and client helpers
├── templates/
│   ├── base.html            # Core layout with M3 styling & Google Fonts
│   ├── home.html            # Public timetable selection screen
│   ├── timetable.html       # Public weekly timetable viewer
│   ├── acc.html             # Legacy account stub
│   └── admin/
│       ├── login.html       # Admin sign-in screen
│       ├── admin_home.html  # Admin control dashboard
│       ├── timetable_mod.html # Timetable editor with add/edit/delete
│       ├── edit_page.html   # Single class edit screen
│       └── create_acc.html  # New admin account creation screen
├── accounts.db              # SQLite database for admin users
├── timetables.db            # SQLite database for class schedules
├── requirements.txt         # Project dependencies including Gunicorn
├── run.py                   # Flask application entry point
└── README.md                # Project documentation
```

---

## 🔐 Administrative Access

Admin credentials are required to modify schedules and create new admin accounts. Access the admin login portal at `/login` or through the **Admin** button in the top navigation.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
