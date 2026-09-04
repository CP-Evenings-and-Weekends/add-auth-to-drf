FROM python:3.13-bookworm

WORKDIR /src

COPY ./requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# CHANGE ME: replace `wines.wsgi:application` with your project's WSGI module
# e.g. `school_proj.wsgi:application` or `publisher.wsgi:application`
CMD gunicorn --bind 0.0.0.0:8000 --workers 3 school_proj.wsgi:application
