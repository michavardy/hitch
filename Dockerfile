# Use the official Python 3.11 image from the Docker Hub
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Create a simple Python script that prints "Hello World"
RUN echo 'print("Hello World")' > hello_world.py

# Set the default command to run the Python script
CMD ["python", "hello_world.py"]
