FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN groupadd user && useradd -m -g user user
USER user
ENV PATH="/home/user/.local/bin:${PATH}"

WORKDIR /app
ADD requirements.txt /app/requirements.txt
ADD requirements_dev.txt /app/requirements_dev.txt
RUN pip install --no-cache-dir --user -r requirements_dev.txt

COPY --chown=user:user . /app

CMD python manage.py runserver 0.0.0.0:8000
