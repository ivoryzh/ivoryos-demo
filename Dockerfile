# Dockerfile (updated)

FROM python:3.10-slim
WORKDIR /app

# Copy all project files
COPY . /app

# Change ownership to allow writing
RUN chmod -R a+w /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose default port
EXPOSE 7860

CMD ["python", "app.py"]
