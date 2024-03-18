FROM selenium/standalone-chrome:latest

# The standalone Selenium Chrome image runs as the selenium user by default
USER root

WORKDIR /app

# Copy only the requirements first to leverage Docker cache
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

CMD ["python", "main.py"]
