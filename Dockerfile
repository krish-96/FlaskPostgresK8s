# Use a slim version of Python for smaller image size
FROM python:3.11-slim

# Add a group and user with specific GID, UID, and custom home directory
ARG GID=5555
ARG UID=5555
ARG HOME_DIR=/home/flaskuser

# Set environment variables for consistent behavior
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/app \
    PATH="${HOME_DIR}/.local/bin:${PATH}"


# Install necessary dependencies and update apt
# Create log directory and ensure permissions for flaskuser
RUN groupadd -g ${GID} flaskgroup \
    && useradd -m -u ${UID} -g flaskgroup -d ${HOME_DIR} flaskuser \
    && apt update && apt install -y \
    # Add any dependencies required for your application here
    && rm -rf /var/lib/apt/lists/* \
    && mkdir -p /var/log/flask \
    && chown -R flaskuser:flaskgroup /var/log/flask \
    && chmod -R 775 /var/log/flask

# Copy the application code and necessary files to the container
COPY FlaskApp /app/FlaskApp
COPY ReleaseNotes /app/ReleaseNotes
COPY requirements.txt /app/


## Upgrade the pip to latest version
#RUN pip install --upgrade pip
#
## Install dependencies from requirements.txt
#RUN pip install --no-cache-dir -r /app/requirements.txt
#
## Ensure the application files are owned by flaskuser and have correct permissions
#RUN chown -R flaskuser:flaskgroup /app/FlaskApp /app/ReleaseNotes /app/requirements.txt \
#    && chmod -R 775 /app/FlaskApp
#
## Switch to flaskuser for better security (non-root user)
#USER flaskuser
#
#
## Verify the user and permissions of the application files (this is optional for debugging)
#RUN whoami
#RUN ls -l /app/FlaskApp
#RUN ls -l /var/log/flask
#

#Added all the above RUN commands into a single command
# Upgrade pip, install dependencies, and set permissions in a single RUN instruction
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt && \
    chown -R flaskuser:flaskgroup /app/FlaskApp /app/ReleaseNotes /app/requirements.txt && \
    chmod -R 775 /app/FlaskApp && \
    whoami && \
    ls -l /app/FlaskApp &&\
    ls -l /var/log/flask


##Commented the below line because it's causing Permission Denied issue
## Switch to flaskuser for better security (non-root user)
#USER flaskuser


# Set the working directory
WORKDIR /app

# Expose the application port
EXPOSE 5052

# Set the entrypoint to run the application
ENTRYPOINT ["python", "FlaskApp/app.py"]
