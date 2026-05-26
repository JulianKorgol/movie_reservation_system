# 🎬 Movie Reservation System

A cinema reservation system built using a microservices architecture and based
on: [Roadmap Task](https://roadmap.sh/projects/movie-reservation-system)

---

## Table of Contents

- [Getting Started](#getting-started)
- [Docs](#docs)
- [Commit Guidelines](#commit-guidelines)
- [Pull Request Guidelines](#pull-request-guidelines)

---

## Getting Started

### Backend, Frontend, Other Docker Containers

```bash
# Clone the repository
git clone https://github.com/JulianKorgol/movie_reservation_system.git
cd movie_reservation_system

# Copy env files
cp envs/.env.nginx.example             envs/.env.nginx
cp envs/.env.microservice-iam.example  envs/.env.microservice-iam
cp envs/.env.postgres-iam.example      envs/.env.postgres-iam
cp envs/.env.frontend-main-app.example envs/.env.frontend-main-app

# Start in development mode
make dev
```

[Documentation list](./docs/README.md)

### Mobile App

To run mobile application, first prepare your enviroment with
docs: [flutter docs](https://docs.flutter.dev/install/quick)

Remember to have Xcode installed: [Xcode App Store link](https://apps.apple.com/us/app/xcode/id497799835?mt=12)

To run project use the commands below:

```bash
# Start flutter in development mode
make dev-mobile-ios #use q to stop

# Shut down & kill iOS emulator
make ios-stop-emulator
```

#### Mobile Requirements

```bash
# Flutter version
flutter doctor
3.41.9

# Xcode (use Apple App Store to check)
26.5
```

---

## Docs

Documentation can be found in the /docs/ folder.
[Documentation list](./docs/README.md)

### API Docs

Every microservice has a Swagger-generated API documentation page:

- [IAM Microservice Swagger Docs](http://localhost/api/iam/admin/docs/)

---

## Commit Guidelines

This project follows [Conventional Commits](https://www.conventionalcommits.org/).
Every commit message must follow this format:

```
type[scope]: short description

[optional body]

[optional footer]
```

### Types

| Type       | When to use                                              |
|------------|----------------------------------------------------------|
| `feat`     | A new feature visible to users or other services         |
| `fix`      | A bug fix                                                |
| `chore`    | Maintenance, tooling, config — no production code change |
| `docs`     | Documentation only                                       |
| `refactor` | Code restructure with no behavior change                 |
| `test`     | Adding or updating tests                                 |
| `devops`   | CI/CD pipeline changes or other DevOps work              |
| `perf`     | Performance improvement                                  |
| `revert`   | Reverting a previous commit                              |

### Scopes

| Scope      | What it covers                                               |
|------------|--------------------------------------------------------------|
| `mobile`   | Mobile application (Flutter)                                 |
| `frontend` | Next.js applications                                         |
| `backend`  | Any backend microservice (use with service name if specific) |

#### Example scopes

| Scope          | What it covers                        |
|----------------|---------------------------------------|
| `iam`          | Auth / identity microservice (Django) |
| `cinema`       | Cinema microservice (FastAPI)         |
| `movie`        | Movie microservice (FastAPI)          |
| `showtime`     | Showtime microservice (FastAPI)       |
| `reservation`  | Reservation microservice (FastAPI)    |
| `notification` | Notification / Celery worker          |
| `nginx`        | Reverse proxy config                  |
| `devops`       | Docker, Compose, infrastructure       |
| `db`           | Database schema, migrations           |
| `deps`         | Dependency updates                    |

### Examples

```bash
# New feature
feat[reservation]: add seat hold expiry via Redis TTL

# Bug fix
fix[iam]: correct JWT expiry calculation for refresh tokens

# DevOps
chore[devops]: add tmpfs mounts to nginx for runtime write access

# Database
chore[db]: add index on reservation.showtime_id

# Documentation
docs[general]: update README with commit guidelines

# Frontend
feat[frontend]: add seat selection UI to booking flow

# Dependency update
chore[deps]: bump next.js from 14.1.0 to 14.2.0

# Revert
revert: feat[reservation]: add seat hold expiry via Redis TTL
```

### Rules

- Use the **imperative mood** in the description: `add`, `fix`, `remove` — not `added`, `fixes`, `removed`
- Keep the first line under **72 characters**
- Do not end the description with a period
- Reference issues in the footer: `Closes #42` or `Refs #17`

---

## Pull Request Guidelines

### Before opening a PR

- [ ] Branch is up to date with `main`
- [ ] All containers start without errors (`make dev`)
- [ ] No secrets or `.env` files committed
- [ ] Commit messages follow the guidelines above
- [ ] Self-review completed — read your own diff before requesting review

### Branch naming

Follow the same `type/scope-short-description` pattern as commits:

```
feat/reservation-seat-hold-expiry
fix/iam-jwt-refresh-expiry
chore/devops-nginx-tmpfs
docs/readme-commit-guidelines
```

### PR size

Keep PRs focused and small. A PR that changes one thing is reviewed faster and is easier to revert if something goes
wrong. If a feature needs multiple services changed, consider splitting into:

1. `chore[db]`: schema / migration PR
2. `feat[backend]`: API endpoint PR
3. `feat[frontend]`: UI PR

---

## Troubleshooting

### Backend microservice not starting up

If one or more microservices fail to start, try resetting the local environment:

```bash
make dev-down
make dev-clean
make dev-build
```

---

Have fun! :)
