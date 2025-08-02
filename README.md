# 📝 Listify - Django Task Manager

Listify is a minimal, functional task management app built with Django. It allows users to create, organize, and manage their tasks by category, priority, and status, with optional email and WhatsApp reminders for overdue tasks.

## 🔗 Live Demo (optional)

> 🟢 Coming soon: [Demo Link Here](https://your-app-name.onrender.com)  
> 💻 Source Code: [GitHub Repo](https://github.com/23CSBS271/listify)

---

## 🚀 Features

- User authentication (Login/Register/Logout)
- Create, update, and delete tasks
- Organize tasks by:
  - Status (Pending/Completed)
  - Priority (High/Medium/Low)
  - Category (Custom-defined)
- Search and filter tasks
- Overdue task email reminders via Gmail SMTP
- WhatsApp SMS reminders via Twilio
- Admin panel to manage users and tasks

---

## 🛠️ Tech Stack

- **Backend**: Django 5.2  
- **Task Queue**: Celery + Redis  
- **Scheduler**: django-celery-beat  
- **Email**: SMTP (Gmail)  
- **WhatsApp**: Twilio API  
- **Database**: SQLite (default)  
- **Frontend**: Django Templates + Bootstrap

---

## ⚙️ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/23CSBS271/listify.git
cd listify


2. Create Virtual Environment
bash
Copy
Edit
python -m venv .venv
.venv\Scripts\activate  # On Windows
3. Install Dependencies
bash
Copy
Edit
pip install -r requirements.txt
4. Set Up Environment Variables
Create a .env file in the root directory:

ini
Copy
Edit
EMAIL_HOST_USER=your_gmail@gmail.com
EMAIL_HOST_PASSWORD=your_app_password
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_WHATSAPP_FROM=whatsapp:+14155238886
Note: Never commit .env to GitHub!

5. Apply Migrations
bash
Copy
Edit
python manage.py migrate
6. Create Superuser (Admin)
bash
Copy
Edit
python manage.py createsuperuser
7. Run the Development Server
bash
Copy
Edit
python manage.py runserver
🕒 Running Celery for Reminders
Make sure Redis is running.

In one terminal:

bash
Copy
Edit
celery -A taskmanager worker --loglevel=info
In another:

bash
Copy
Edit
celery -A taskmanager beat --loglevel=info
📂 Project Structure (Simplified)
bash
Copy
Edit
listify/
├── core/               # Django app
│   ├── models.py
│   ├── views.py
│   └── templates/
├── taskmanager/        # Project settings
├── static/             # CSS, JS, Icons
├── .env                # Environment variables (not committed)
├── manage.py
└── requirements.txt
🙋‍♂️ Auth
