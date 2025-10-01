# Movie Reservation System

A web system built for cinema owners to manage movies and reservations efficiently.

API docs: http://localhost:8000/docs/ (require backend running)

## 🔦 Requirements

### Backend

```bash
python3 -v
3.12.3
```

### Frontend

```bash
node -v
>= 18.17.0
npm -v
>= 9.0.0
```

## 💻 How to run

### Development

#### Backend

```bash
pip install -r backend/requirements.txt
cd backend
python manage.py makemigrations
python manage.py migrate
 python manage.py dev_db # Load Development data
python manage.py runserver
```

#### Frontend

```bash
npm install
npm run dev
```

## ⏳ GitLab Flow

We follow GitLab Flow best practices for collaboration.

GitLab Flow combines Git Flow and GitHub Flow by adding environment-specific branches, making it easier to track
deployments while staying simpler than full Git Flow.

### Branch-es

`main` branch is always stable, deployable

`production` branch is to integrate all features for the next release

`type/<short-description>` branches are for specific features, fixes, chores, or docs

### Branch syntax

We use clear prefixes for branches:

- `feat/<short-description>` -> new features
- `chore/<short-description>` -> maintenance tasks that don’t affect app features or docs
- `fix/<short-description>` -> bug fixes
- `docs/<short-description>` -> documentation changes

## 📝 Commit Message Guidelines

We enforce **Conventional Commits** using [commitlint](https://commitlint.js.org/).  
This ensures consistency and makes it easier to generate changelogs and track changes.

### ✅ Commit Message Format

Each commit message should be structured as:

```
<type>: <short, lowercase description>
[optional body]
[optional footer(s)]
```

Examples:

- `feat: add user login API`
- `fix: correct typo in README`
- `chore: update dependencies`
- `docs: add contribution guide`

### Allowed commit types

- **feat** → new features
- **fix** → bug fixes
- **chore** → maintenance tasks that don’t affect app features or docs
- **docs** → documentation changes
- **refactor** → code restructuring without changing behavior
- **test** → add or fix tests

### Rules

- Subject **must not** be empty
- Subject **must** be in **lowercase**
- Max length: **100 characters**

⚠️ Commits that don’t follow this format will be **rejected** by Husky + commitlint.

<b>Remember to run `npm i` in root directory after cloning the repo to install Husky.</b>

## 🏃 User Flow

Possible user flow to interact with the system.

### General Reservation Process

<b>Goal:</b> Allow a customer to browse available movies, select a showtime, reserve specific seats, and complete the
reservation.

Flow steps:

1. Select Cinema Location
    - User selects preferred cinema from a list of available locations.

2. Choose movie and showtime
    - User views list of movies playing at the chosen location.
    - User selects a movie → shows all available showtimes (with date, time).
        - User should be able to see movie list with showtimes on one page.

3. Select ticket type and seat
    - User chooses desired number and type of tickets (Standard, VIP, Student, etc.).
    - Seat map is displayed for chosen showtime.
    - User selects seats on the map.
        - Backend should lock (hold) these seats temporarily to prevent over-booking.
        - Backend returns a temporary reservation token

4. Review reservation summary
    - User reviews selected movie, showtime, seats, ticket type, and price breakdown.
    - Option to go back and modify selection.

5. Confirm reservation
    - User confirms reservation → backend finalizes booking.
    - Backend checks if seat locks are still valid, then marks them as reserved.
    - Reservation record is stored, and confirmation email is sent.
    - Optional: Redirect to payment gateway (if enabled).

#### Seat Hold Mechanism (Critical Logic)

- When a user selects a seat, the frontend must call the backend to lock/hold that seat.
- Backend stores the lock in DB with a short expiration (e.g., 5 minutes).
- If the user confirms within the expiration window, the reservation is created and the hold is converted into a
  booking.
- If the lock expires, the seats are released and become available again.
    - Do not show to User (Flow) that seats hold expired if the token expires and seats are still free to take (user is
      still in the reservation process).

### Home Page

- Welcome header + (easy) branding.
- Location selector → leads to available movies page.

### User Dashboard Page

<b>Goal:</b> Access to reservations and user data management.

Features:

1. Login panel
    - User can log in.
    - E-mail verification flow

2. Manage Reservations
    - View upcoming and past reservations.
    - Cancel upcoming reservations (if allowed by rules).
    - Download reservation ticket (PDF/QR code).
    - See reservation history.

### Admin Dashboard Page

<b>Goal:</b> Allow admins to manage all data.

Features:

1. Login panel
    - Admin login with 2FA (optional)

2. Movie and Showtime Management
    - CRUD operations for Movies (title, description, poster, genre, etc.).
    - CRUD operations for Theaters and Rooms (seat layout configuration).
    - Create/edit/delete Showtimes linked to specific theaters.
    - Adjust seats and add more rooms dynamically.

3. Weekly Scheduling
    - Create a complete schedule for the upcoming week.
    - Assign movies to timeslots and theaters.

4. Users Management
    - View all registered users.
    - Promote/demote users (assign admin role).
    - Deactivate/ban users.

5. Reservations Management
    - View all reservations.
    - Cancel any reservation.
    - See reservation details (user, showtime, seats).
    - View seat capacity per room.
    - View revenue reports (by showtime/date/movie). (optional, but wanted by idea creator)

## 🔒 Security

### URLs

List of URLs that should have restricted (or locked) access in production:

- `/admin/`
- `/docs/`
- `/schema/`
