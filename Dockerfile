# Step 1: Use an official Python runtime as a base image
FROM python:3.10-slim as builder

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install the required dependencies including 'dev' dependencies required for building the app
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Step 2: Prepare production image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Copy only the necessary files from the builder stage
COPY --from=builder /app /app

# Install only production dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Use arguments to set environment variables
ARG DB_URI
ARG MAIL_SMTP_LOGIN
ARG MAIL_SMTP_PASSWORD
ARG MAIL_SMTP_SERVER
ARG MAIL_SMTP_PORT
ARG MAIL_FROM_EMAIL

# Set environment variables
ENV DB_URI=${DB_URI}
ENV MAIL_SMTP_LOGIN=${MAIL_SMTP_LOGIN}
ENV MAIL_SMTP_PASSWORD=${MAIL_SMTP_PASSWORD}
ENV MAIL_SMTP_SERVER=${MAIL_SMTP_SERVER}
ENV MAIL_SMTP_PORT=${MAIL_SMTP_PORT}
ENV MAIL_FROM_EMAIL=${MAIL_FROM_EMAIL}

# Expose port 8000
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
