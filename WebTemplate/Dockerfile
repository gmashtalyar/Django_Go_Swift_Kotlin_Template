FROM python:3.11-slim

WORKDIR /app
RUN apt-get update && apt-get install -y curl && apt-get clean

COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

COPY . /app/



CMD python3 manage.py makemigrations \
    && python3 manage.py migrate \
    && python3 manage.py shell -c "import os; from django.contrib.auth import get_user_model; User = get_user_model(); username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin'); User.objects.filter(username=username).exists() or User.objects.create_superuser(username, os.environ.get('DJANGO_SUPERUSER_EMAIL', ''), os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'changeme'))" \
    && python3 manage.py collectstatic --no-input \
    && gunicorn -w 4 django_project.wsgi:application --bind 0.0.0.0:8000
