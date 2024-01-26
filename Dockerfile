# Setting base image
FROM python:3.11.0

# Set working directory
WORKDIR .

# Copying the application into the container
COPY . .

# Installling dependencies
RUN pip install --upgrade pip
RUN pip install -r src/requirements.txt