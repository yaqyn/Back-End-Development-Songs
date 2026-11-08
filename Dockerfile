FROM python:3.11-slim

WORKDIR /opt/app-root/src

COPY requirements.txt /opt/app-root/src/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /opt/app-root/src

EXPOSE 8080
ENV FLASK_APP=app
ENV PORT=8080

CMD ["gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
