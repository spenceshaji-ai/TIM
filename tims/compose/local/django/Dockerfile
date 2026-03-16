# define an alias for the specific python version used in this file.
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS python

# Python build stage
FROM python AS python-build-stage

ARG APP_HOME=/app

WORKDIR ${APP_HOME}

# move virtualenv outside overridden mount directory
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy UV_PYTHON_DOWNLOADS=0

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  build-essential \
  libpq-dev \
  gettext \
  wait-for-it

# Copy dependency files first for caching
COPY pyproject.toml uv.lock ./

# Install dependencies (without installing project itself yet)
RUN uv sync --no-install-project

# Copy the rest of the project
COPY . ${APP_HOME}

# Install project dependencies
RUN uv sync

# devcontainer utilities
RUN apt-get update && apt-get install --no-install-recommends -y \
  sudo git bash-completion nano ssh

# Create devcontainer user
RUN groupadd --gid 1000 dev-user \
  && useradd --uid 1000 --gid dev-user --shell /bin/bash --create-home dev-user \
  && echo dev-user ALL=\(root\) NOPASSWD:ALL > /etc/sudoers.d/dev-user \
  && chmod 0440 /etc/sudoers.d/dev-user

ENV PATH="/${APP_HOME}/.venv/bin:$PATH"
ENV PYTHONPATH="${APP_HOME}/.venv/lib/python3.13/site-packages:$PYTHONPATH"

# Copy entrypoint
COPY ./compose/production/django/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint && chmod +x /entrypoint

# Copy start script
COPY ./compose/production/django/start /start
RUN sed -i 's/\r$//g' /start && chmod +x /start

ENTRYPOINT ["/entrypoint"]