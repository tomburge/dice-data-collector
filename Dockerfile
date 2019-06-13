FROM python:alpine3.7
COPY . /app
WORKDIR /app
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
EXPOSE 8000
# CMD python ./app.py
CMD ["gunicorn", "--workers=2", "--timeout", "1800", "--threads=2", "--worker-class=gthread", "-b", "0.0.0.0:8000", "wsgi"]
