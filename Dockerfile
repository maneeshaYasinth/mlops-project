# Step 1: Start from an official Python base images
FROM python:3.11-slim

# Step 2: Set the "working directory" inside the container
WORKDIR /app

# Step 3: Copy the requirements file into the container
COPY requirements.txt .

# Step 4: Install the Python libraries
RUN pip install --no-cache-dir -r requirements.txt

# Step 5: Copy the rest of your application code into the container
COPY . .

# Step 6: Expose the port that Flask runs on
EXPOSE 5000

# Step 7: Define the command to run your application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]