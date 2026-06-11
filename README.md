# Online Courses Platform: Design Patterns Course Project

FastAPI application for a small LMS platform. The goal is to demonstrate 9 design patterns in real application scenarios: course creation, profile customization, avatar upload, test building, test passing, notifications, external LMS integration and dashboard.

## Run

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open:

- Web UI: http://127.0.0.1:8000
- API docs: http://127.0.0.1:8000/docs

SQLite database is created automatically as `app.db`.

## Implemented Patterns

| Type | Pattern | Files | Real use in the system |
|---|---|---|---|
| Creational | Factory Method | `app/domain/patterns/factory_method.py` | Creates video, text and interactive courses without coupling routers to concrete course classes. |
| Creational | Abstract Factory | `app/domain/patterns/abstract_factory.py` | Creates question objects together with compatible answer checkers. |
| Creational | Builder | `app/domain/patterns/builder.py` | Builds a test from course, selected questions, time limit, pass score and attempts. |
| Structural | Adapter | `app/domain/patterns/adapter.py` | Integrates Moodle and Google Classroom through one `enroll()` interface. |
| Structural | Decorator | `app/domain/patterns/decorator.py` | Extends a user profile with avatar, theme and badges. |
| Structural | Facade | `app/domain/patterns/facade.py` | Provides one enrollment operation that touches users, courses, enrollments, notifications and activity logs. |
| Behavioral | Strategy | `app/domain/patterns/strategy.py` | Selects questions by easy, medium, hard or adaptive algorithms. |
| Behavioral | Observer | `app/domain/patterns/observer.py` | Sends notifications after test submission to console channels and database. |
| Behavioral | Command | `app/domain/patterns/command.py` | Encapsulates user actions such as changing theme, uploading avatar and adding badges, then logs them. |

## Main Scenarios

1. Create courses on `/pages/courses`.
2. Enroll demo user `1` into a course from the same page.
3. Create questions and build tests on `/pages/tests`.
4. Use `/tests/{test_id}/submit?user_id=1` to submit answers through API.
5. Upload avatar and switch profile theme on `/pages/profile`.
6. Check enrollments and notifications on `/pages/dashboard`.
7. Test external LMS adapters on `/pages/integration`.

## Authentication

The web UI has a simple local authentication flow:

- Login/register page: `/pages/auth`
- Demo email: `student@example.com`
- Demo password: `demo`

After login the app stores `user_id` in an HTTP-only cookie and uses it for profile settings, avatar upload, dashboard and course enrollment.

## Architecture

- `app/domain/entities` contains business objects.
- `app/domain/patterns` contains pattern implementations.
- `app/domain/services` contains application logic.
- `app/repositories` contains SQLite persistence logic.
- `app/routers` contains FastAPI endpoints and page actions.
- `app/templates` and `app/static` contain UI assets.
