# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /usr/src/app

# Install poetry
RUN pip install poetry

# Copy the project files (including pyproject.toml for poetry)
COPY . .

# Install dependencies via poetry
RUN poetry install --no-dev

# Create a directory for the service account JSON file
RUN mkdir -p /root/.gcp/

# Copy the service account JSON file from your secrets directory
# Adjust the path './secrets/service-account.json' if necessary
COPY ./secrets/service-account-drive.json /root/.gcp/service-account-drive.json

# Expose the port the app runs on
EXPOSE 8080

# Define the command to run the app
CMD ["uvicorn", "superboite_api.main:app", "--host", "0.0.0.0", "--port", "8080"]
