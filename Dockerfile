FROM python:3.8-alpine
WORKDIR /python3-web-app-project
COPY python3-web-app-project/requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY python3-web-app-project/ .
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
