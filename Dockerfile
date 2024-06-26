# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Install any needed packages specified in requirements.txt
# If you don't have a requirements.txt file, you can skip this step
RUN pip install --no-cache-dir -r requirements.txt

# Run the script when the container launches
CMD ["python", "./runner.py"]
