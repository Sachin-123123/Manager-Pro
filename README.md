# ToDoManagement

A modern task management application built with Django and Tailwind CSS.

## Features

- Personal To-Do Lists
- Organizational Task Management
- Team Collaboration
- Calendar View
- Real-time Notifications
- User Authentication
- Responsive Design

## Tech Stack

- Django 5.0.2
- Python 3.12
- Tailwind CSS
- SQLite (Development)
- FullCalendar.js

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/todomanagement.git
cd todomanagement
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create a superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Usage

1. Access the application at `http://127.0.0.1:8000`
2. Log in with your credentials
3. Start managing your tasks and organizations

## Project Structure

```
todomanagement/
├── core/                 # Main application
│   ├── models.py        # Database models
│   ├── views.py         # View logic
│   ├── urls.py          # URL routing
│   └── templates/       # HTML templates
├── todomanagement/      # Project settings
├── static/             # Static files
└── manage.py           # Django management script
```
