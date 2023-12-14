FROM python:3.9.2-slim
WORKDIR /usr/src/app
COPY . /usr/src/app
RUN pip install -r requirements.txt
RUN mkdir -p /root/.gcp/
COPY ./secrets/service-account-drive.json /root/.gcp/service-account-drive.json
EXPOSE 8080

# Define the command to run the app
CMD ["poetry", "run", "uvicorn", "superboite_api.main:app", "--host", "0.0.0.0", "--port", "8080"]
