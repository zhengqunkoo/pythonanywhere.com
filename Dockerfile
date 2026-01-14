FROM python:3.13-slim
LABEL maintainer="zhengqun.koo@gmail.com"

# Use pipenv to manage a project-local virtualenv and run as a non-root user.
WORKDIR /workdir
COPY . /workdir

# Install pipenv (system-wide), create a non-root user, and set ownership.
RUN python -m pip install --upgrade pip \
	&& python -m pip install --no-cache-dir pipenv \
	&& useradd -m -s /bin/bash flaskuser \
	&& chown -R flaskuser:flaskuser /workdir

USER flaskuser

# Ensure the virtualenv is created inside the project directory (.venv)
ENV PIPENV_VENV_IN_PROJECT=1

# Install dependencies into the project-local virtualenv using pipenv.
RUN pipenv install -r requirements.txt

#EXPOSE 80
ENTRYPOINT ["pipenv", "run", "python"]
CMD ["main.py"]