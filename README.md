# Movie Reservation System

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

## 🏃 How to run

### Development

#### Backend

```bash
pip install -r backend/requirements.txt
cd backend
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

- `feature/<short-description>` -> new features
- `chore/<short-description>` -> maintenance tasks that don’t affect app features or docs
- `fix/<short-description>` -> bug fixes
- `docs/<short-description>` -> documentation changes

## 🔒 Security

- `admin/` -> Should be locked on production.
- `docs/` -> Should be locked on production.
- `schema/` -> Should be locked on production.

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