# Use an official Python runtime as a parent image
FROM python:3.8

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . /usr/src/app

# Install any needed packages specified in pyproject.toml (Poetry)
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

# Make port 80 available to the world outside this container
EXPOSE 8080

# Run app.py when the container launches
CMD ["uvicorn", "superboite_api.main:app", "--host", "0.0.0.0", "--port", "8080"]
