# Electives-II-Assignment-1
Assignment Overview You are to apply the interaction design process and develop a conceptual model and  Django-based wireframe for a context-aware mobile or web application that supports  community health and fitness needs (e.g., workout tracking, meal planning, water intake  reminders, wellness check-ins).
FitBuddy Django Wireframe
This repository contains a functional Django wireframe for the FitBuddy application. It demonstrates the core backend components required to support a health and fitness tracking app.

Project Structure
fitbuddy_project/: The main Django project directory.

fitbuddy/: The Django application containing the models, views, templates, and URLs.

templates/fitbuddy/: Contains all the HTML templates for the app.

Features
User Authentication: User registration and login functionality.

Data Models: Models for Users, Activities, Sessions, Bookings, and various logs (Hydration, Activity).

Core Functionality:

Dashboard view for logged-in users.

Activity browsing and detail views.

Session booking and cancellation.

Hydration and activity logging via dedicated endpoints.

Setup and Running
Clone the repository:



Create a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:

pip install Django

Apply migrations:

python manage.py makemigrations
python manage.py migrate

Create a superuser:

python manage.py createsuperuser

Run the development server:

python manage.py runserver

