FROM python:3.10-slim

ENV APP_HOME /app
WORKDIR $APP_HOME

# Removes output stream buffering, allowing for more efficient logging
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# COPY tiara_23_backend $APP_HOME/tiara_23_backend/

# Copy local code to the container image.
COPY . .

WORKDIR $APP_HOME/
CMD exec gunicorn --bind 8000:8000 --workers 1 --threads 8 --timeout 0 hackverse_4.wsgi:application