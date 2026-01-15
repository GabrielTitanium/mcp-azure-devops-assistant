# Use a stable Python image
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Copy dependency list first (Docker best practice)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Run the MCP server
CMD ["python", "server.py"]
