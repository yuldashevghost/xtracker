# Habit Tracker Website

A fully functional Habit Tracker built with Django, featuring a dark theme with black background and bright blue accents.

## Features

- ✅ User Authentication (Register, Login, Logout)
- ✅ Habit Management (Add, Edit, Delete)
- ✅ Automatic Daily Task Generation
- ✅ Task Completion Tracking
- ✅ Performance Statistics & Analytics
- ✅ Responsive Design (Mobile, Tablet, Desktop)
- ✅ Dark Theme with Blue Accents
- ✅ Smooth Animations & UI Interactions

## Default Habits

When a new user registers, they automatically receive these default habits:
- Wake up at a specific morning time (07:00)
- Running / Exercise (08:00)
- Working / Studying (09:00)
- Reading a book (19:00)

## Installation

1. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations (if not already done):**
   ```bash
   python manage.py migrate
   ```

4. **Create a superuser (optional, for admin access):**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

6. **Access the application:**
   - Open your browser and go to: `http://127.0.0.1:8000/`

## Manual Task Generation

**Tasks are NOT automatically generated.** Users have full control and can manually generate tasks for any date they choose.

### How to Generate Tasks

1. **From the Dashboard:**
   - Click the "Generate Tasks" button
   - Select a date from the date picker
   - Click "Generate Tasks" to create tasks for that date based on your habits
   - Or click "Generate for Today" for a quick action

2. **Via Management Command (Optional):**
   For bulk operations or automation, you can use the management command:
   ```bash
   python manage.py generate_daily_tasks
   ```
   
   Generate for a specific date:
   ```bash
   python manage.py generate_daily_tasks --date 2024-01-15
   ```
   
   Generate for today and past days:
   ```bash
   python manage.py generate_daily_tasks --days-back 7
   ```

## Project Structure

```
xtracker/
├── habit_tracker/          # Django project settings
├── tracker/                # Main app
│   ├── models.py          # Habit and DailyTask models
│   ├── views.py           # All views
│   ├── utils.py           # Task generation utilities
│   ├── signals.py         # Default habits creation
│   └── management/
│       └── commands/
│           └── generate_daily_tasks.py  # Daily task generation command
├── templates/             # HTML templates
│   ├── base.html
│   ├── auth/             # Login/Register
│   └── dashboard/        # Dashboard, Habits, Stats
├── static/               # Static files
│   ├── css/
│   │   └── style.css    # Dark theme styles
│   └── js/
│       └── main.js      # Animations & interactions
└── requirements.txt
```

## Usage

1. **Register a new account** or **login** with existing credentials
2. **View your dashboard** to see today's tasks
3. **Manage habits** from the Habits page
4. **Track your progress** on the Statistics page
5. **Mark tasks as complete** by checking the checkbox

## Technologies Used

- Django 5.2.8
- HTML5
- CSS3 (with CSS Grid & Flexbox)
- JavaScript (Vanilla JS)
- SQLite Database

## Responsive Breakpoints

- **Desktop**: Default layout with sidebar navigation
- **Tablet** (≤768px): Grid layout adjustments
- **Mobile** (≤480px): Stacked layout, full-width buttons

## Notes

- **Tasks are NOT automatically generated** - users must manually generate tasks for dates they want to track
- Tasks are generated based on your habits for the selected date
- Each user has separate habits and tasks
- Tasks are grouped by date on the dashboard
- Statistics are calculated in real-time
- You can generate tasks for any date (past, present, or future)
