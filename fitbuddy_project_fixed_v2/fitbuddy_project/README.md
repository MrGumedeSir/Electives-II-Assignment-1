
# FitBuddy (fixed v2)

This packaged FitBuddy project includes fixes for structure, models, views, and accessibility improvements.

## Quick start (local)

1. Create venv and activate
2. pip install -r requirements.txt
3. python manage.py makemigrations
4. python manage.py migrate
5. python manage.py createsuperuser  # optional
6. python manage.py runserver
7. Open http://127.0.0.1:8000/

## Accessibility improvements included
- Skip link to jump to main content
- aria-live region for system messages
- Form inputs annotated with aria-labels
- Images given alt text placeholders
- Templates organized under templates/fitbuddy/

## Tests and next steps
- Run `python manage.py test` after adding tests (a tests scaffold exists)
- Improve contrast and add keyboard focus styles
