# TaskFlow

**Organise your day. Finish what matters.**

TaskFlow is a modern, multi-user to-do and task manager built with **Django**. It gives every user their own private workspace, with a clean dashboard that shows what's due today, what's overdue and what's coming up this week, all at a glance.

Tasks can have a description, a priority (Low, Medium or High), a due date and a colour-coded category such as Work, Personal or Shopping. You can search, filter and sort them in seconds, tick them off with one click, and watch your progress grow on a weekly chart and a completion ring.

TaskFlow was built to show that a polished, professional web app doesn't need a heavy frontend framework. The whole interface is Django templates, hand-written CSS and a few lines of vanilla JavaScript. It's fully responsive on phones, switches to dark mode automatically, and is backed by Django's built-in authentication, so each user's data stays private.

**Who it's for:** anyone who wants a simple, distraction-free place to plan their work and personal tasks, and developers looking for a clean, well-structured Django project to learn from or build on.

![TaskFlow dashboard](screenshots/dashboard.png)

---

## Features

**Dashboard**
- Stat cards for total, completed, in-progress and overdue tasks
- Quick-add bar to create a task in seconds
- Overdue, due-today and coming-this-week lists
- Overall progress ring and a "completed this week" bar chart
- Progress by category and recently completed tasks

**Tasks**
- Create, edit, delete and mark tasks as done
- Title, description, category, priority (Low / Medium / High) and due date
- Filter by All, Active, Today, Upcoming, Overdue and Completed
- Filter by priority and category, sort by due date, priority or newest
- Search across task titles and descriptions
- Overdue tasks highlighted automatically
- Clear all completed tasks in one click

**Categories**
- Create colour-coded categories (Work, Personal, Shopping, etc.)
- Category counts in the sidebar
- Deleting a category keeps its tasks

**Accounts**
- Sign up, log in and log out
- Each user only sees their own tasks
- Profile page to update name, email and password

**Design**
- Clean, responsive layout that works on desktop and mobile
- Automatic dark mode
- Toast notifications for every action
- No CSS framework or build tools: plain HTML, CSS and a little JavaScript

---

## Screenshots

| Login | Task list |
|---|---|
| ![Login](screenshots/login.png) | ![Tasks](screenshots/tasks.png) |

| Categories | Mobile |
|---|---|
| ![Categories](screenshots/categories.png) | ![Mobile](screenshots/mobile.png) |

---

## Tech stack

- **Backend:** Python, Django
- **Database:** SQLite
- **Frontend:** Django templates, HTML, CSS, vanilla JavaScript
- **Auth:** Django's built-in authentication

---

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/Netlution/taskflow.git
cd taskflow
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows:

```bash
venv\Scripts\activate
```

macOS / Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up the database

```bash
python manage.py makemigrations todo
python manage.py migrate
```

### 5. (Optional) Create an admin account

```bash
python manage.py createsuperuser
```

### 6. Run the server

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser, create an account and start adding tasks.

---

## Project structure

```
taskflow/
├── config/                   # Project settings and root URLs
├── todo/
│   ├── models.py             # Todo and Category models
│   ├── views.py              # Dashboard, tasks, categories, profile
│   ├── forms.py              # Sign-up, task, category and profile forms
│   ├── urls.py               # App routes
│   ├── context_processors.py # Sidebar counts on every page
│   ├── templatetags/         # Custom {% icon %} tag
│   ├── static/todo/          # style.css and app.js
│   └── templates/            # All HTML templates
├── screenshots/              # Images used in this README
├── manage.py
└── requirements.txt
```

---

## Author

Built by **Netlution**

- GitHub: [@Netlution](https://github.com/Netlution)
- Email: ajagunsamuel2017@gmail.com

---

## License

This project is open source and available for personal and educational use.
