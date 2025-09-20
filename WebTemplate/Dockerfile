FROM python:3.11-slim

WORKDIR /app
RUN apt-get update && apt-get install -y curl && apt-get clean

COPY requirements.txt /app/
RUN pip3 install -r requirements.txt

COPY . /app/



CMD python3 manage.py makemigrations \
    && python3 manage.py migrate \
    && python3 manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='Gennady').exists() or User.objects.create_superuser('Gennady', '', '3957Crew@!')" \
    && python3 manage.py collectstatic --no-input \
    && gunicorn -w 4 django_project.wsgi:application --bind 0.0.0.0:8000
