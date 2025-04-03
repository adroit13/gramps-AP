# Use an official Python image
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gramps

# Copy your GrampsWeb API project files
COPY . /app

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port GrampsWeb API will run on
EXPOSE 5000

# Start the API
CMD ["grampsweb", "run"]
 
