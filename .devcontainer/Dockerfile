# Use official Playwright base image (Ubuntu 22.04, Python + browsers included)
FROM mcr.microsoft.com/playwright/python:v1.48.0-jammy

# Copy requirements and install your libs
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt
