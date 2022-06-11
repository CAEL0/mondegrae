# ------------------------------------------------------------------------------
# Base image
# ------------------------------------------------------------------------------
FROM python:3.8-slim AS base

# ------------------------------------------------------------------------------
# Install dependencies
# ------------------------------------------------------------------------------
FROM base AS deps
COPY requirements.txt ./
RUN apt update > /dev/null && \
        apt install -y build-essential && \
    apt-get -y install libgl1-mesa-glx && \
    apt install -y default-jre && \
    apt install -y default-jdk && \
        pip install --disable-pip-version-check -r requirements.txt --no-cache-dir

# ------------------------------------------------------------------------------
# Final image
# ------------------------------------------------------------------------------
FROM deps
WORKDIR /usr/src/app
COPY . /usr/src/app

EXPOSE 80

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

