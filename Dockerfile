FROM python:3.11

# Create necessary directories and set permissions
RUN mkdir -p /var/log/flask && chmod -R 777 /var/log/flask

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY FlaskApp /app/FlaskApp
COPY ReleaseNotes /app/ReleaseNotes

# Set PYTHONPATH for the FlaskApp package
ENV PYTHONPATH=/app

EXPOSE 5052

#CMD ["python", "FlaskApp/app.py"]

ENTRYPOINT ["python", "FlaskApp/app.py"]
