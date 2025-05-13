FROM python:3.11-slim-bookworm AS builder

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates

# Download and run the UV installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh
RUN sh /uv-installer.sh && rm /uv-installer.sh

FROM python:3.11

COPY --from=builder /root/.local/bin/uv /root/.local/bin/uv

# add UV to path
ENV PATH="/root/.local/bin/:$PATH"

# Install google chrome browser
RUN apt-get -qq update && \
    apt-get -qq install wget && \
    wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt -qq install -y ./google-chrome-stable_current_amd64.deb && \
    rm google-chrome-stable_current_amd64.deb

WORKDIR /app

COPY pyproject.toml .

COPY uv.lock .

RUN uv sync --locked

COPY src/ .

ENTRYPOINT ["uv", "run"]