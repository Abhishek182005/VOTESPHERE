# VoteSphere — Django Polling Application

A full-featured polling web application built with **Django 5** and **Bootstrap 5**. VoteSphere lets admins create and manage polls while registered users can cast votes, view live results, and participate in transparent, one-vote-per-user elections.

---

## Screenshots

| Home | Vote | Results | Admin Dashboard |
|------|------|---------|-----------------|
| Poll listing with option previews | Radio-button vote card | Color-coded progress bars | Stat cards + poll management table |

---

## Features

### For Regular Users
- **Register & Login** — Secure account creation and authentication
- **Browse Active Polls** — See all live polls on the home page with a preview of the options
- **Cast a Vote** — Select one of three options per poll; each user can only vote once per poll
- **View Results** — See vote counts, percentages, and the winner highlighted with a trophy badge (only when the admin publishes results, or always for admins)
- **Vote History** — The home page marks polls you've already voted in

### For Admins (Staff Users)
- **Create Polls** — Add a question and exactly three answer options
- **Dashboard** — Overview of total polls, active polls, and total votes cast
- **Publish / Unpublish Results** — Control when regular users can see the outcome of a poll
- **Open / Close Polls** — Toggle whether a poll is accepting new votes
- **Voters List** — View every voter and their choice for any poll, with timestamps
- **Delete Polls** — Remove a poll and all associated votes with a confirmation step
- **Django Admin Panel** — Full access to the built-in `/admin/` interface

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.11, Django 5.0.6 |
| Frontend | Bootstrap 5.3.3, Bootstrap Icons 1.11.3 |
| Database | SQLite (default), easily swappable to PostgreSQL/MySQL |
| Auth | Django's built-in `django.contrib.auth` |
| Template Engine | Django Templates with `widget_tweaks` |

---

## Project Structure

```
POLLING-DJANGO/
├── manage.py
├── db.sqlite3
├── write_templates.py        # Utility: restores all templates from source
│
├── poll/                     # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py / asgi.py
│
├── poll_portal/              # Main app
│   ├── models.py             # Poll + Vote models
│   ├── views.py              # All view logic
│   ├── forms.py              # PollForm, UserRegisterForm
│   ├── admin.py              # Admin registration
│   ├── urls.py               # App URL patterns
│   ├── migrations/
│   └── templates/
│       └── poll_portal/
│           ├── base.html           # Shared layout, navbar, footer
│           ├── home.html           # Poll listing
│           ├── vote.html           # Vote form
│           ├── results.html        # Result bars + winner
│           ├── create.html         # Create poll (admin)
│           ├── delete.html         # Delete confirmation (admin)
│           ├── admin_dashboard.html# Dashboard (admin)
│           ├── voters.html         # Voters list (admin)
│           ├── login.html
│           └── register.html
│
└── myvenv/                   # Python virtual environment
```

---

## Data Models

### `Poll`
| Field | Type | Description |
|---|---|---|
| `question` | TextField | The poll question |
| `option_one/two/three` | CharField | The three answer choices |
| `option_one/two/three_count` | IntegerField | Vote tallies |
| `pub_date` | DateTimeField | Creation timestamp |
| `is_active` | BooleanField | Whether the poll accepts votes |
| `result_published` | BooleanField | Whether results are public |
| `created_by` | ForeignKey(User) | Admin who created it |

### `Vote`
| Field | Type | Description |
|---|---|---|
| `user` | ForeignKey(User) | Who voted |
| `poll` | ForeignKey(Poll) | Which poll |
| `choice` | CharField | `'option1'`, `'option2'`, or `'option3'` |
| `voted_on` | DateTimeField | When the vote was cast |

> `unique_together = ('user', 'poll')` enforces one vote per user per poll at the database level.

---

## URL Routes

| URL | View | Access |
|---|---|---|
| `/` | Home — poll listing | Public |
| `/vote/<id>/` | Cast a vote | Authenticated |
| `/results/<id>/` | View results | Published or Admin |
| `/register/` | Create account | Anonymous only |
| `/login/` | Sign in | Anonymous only |
| `/logout/` | Sign out | Authenticated |
| `/create/` | Create a new poll | Admin only |
| `/delete/<id>/` | Delete a poll | Admin only |
| `/dashboard/` | Admin dashboard | Admin only |
| `/voters/<id>/` | Voters list for a poll | Admin only |
| `/declare/<id>/` | Toggle result visibility | Admin only |
| `/toggle-active/<id>/` | Open/close a poll | Admin only |
| `/admin/` | Django admin panel | Admin only |

---

## Setup & Installation

### 1. Clone the repository
```bash
git clone https://github.com/Abhishek182005/POLLAPP.git
cd POLLAPP
```

### 2. Create and activate a virtual environment
```bash
# Windows
python -m venv myvenv
myvenv\Scripts\activate

# macOS / Linux
python -m venv myvenv
source myvenv/bin/activate
```

### 3. Install dependencies
```bash
pip install django==5.0.6 django-widget-tweaks
```

### 4. Apply migrations
```bash
python manage.py migrate
```

### 5. Create a superuser (admin account)
```bash
python manage.py createsuperuser
```

### 6. Run the development server
```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000/** in your browser.

---

## Usage Guide

### As an Admin
1. Log in with your superuser credentials at `/login/`
2. Go to **Dashboard** from the navbar to see all polls and stats
3. Click **New Poll** to create a poll — enter a question and three options
4. After votes come in, click the 👁 icon in the dashboard to **publish results** for everyone
5. Use the ⏹ icon to **close** a poll when voting should stop
6. View who voted and what they chose via the 👥 icon

### As a Regular User
1. Register at `/register/` or log in at `/login/`
2. Browse active polls on the home page
3. Click **Vote** on any poll you haven't voted in yet
4. Once results are published by an admin, click **Results** to see the outcome

---

## Utility Script

If the VS Code HTML formatter breaks Django template tags (`{% %}`), restore all templates by running:

```bash
python write_templates.py
```

This overwrites all 10 templates with their correct content.

---

## License

This project is open source and available under the [MIT License](LICENSE).
