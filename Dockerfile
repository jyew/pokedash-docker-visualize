FROM python:3.8-slim-buster

# Create a working directory.
RUN mkdir wd
WORKDIR wd

# Install Python dependencies.
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy the rest of the codebase into the image
COPY . ./

USER 1001

# Finally, run gunicorn.
CMD ["python", "./app.py"]