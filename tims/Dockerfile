FROM python:3.11-slim

WORKDIR /app

# Copy dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=tims.settings.prod
ENV DEBUG=False

# Run Django with Gunicorn
CMD ["gunicorn", "TIMS.wsgi:application", "--bind", "0.0.0.0:8000"]