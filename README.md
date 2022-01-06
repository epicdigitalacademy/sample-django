# Preparing Django app
1. `python3 manage.py migrate`
2. `python3 manage.py collectstatic`
3. `python3 manage.py createsuperuser`

# Running with SigNoz
```
pip3 install -r requirements.txt
```

```
opentelemetry-bootstrap --action=install
```

## To run with gunicorn you need to add post_fork hook
1. add a file `gunicorn.config.py` as given in this repo
2. specify that config file when running gunicorn as in below run command

```
DJANGO_SETTINGS_MODULE=<DJANGO_APP>.settings  OTEL_RESOURCE_ATTRIBUTES=service.name=<serviceName> OTEL_EXPORTER_OTLP_ENDPOINT="http://<IP OF SigNoz>:4317" opentelemetry-instrument gunicorn <DJANGO_APP>.wsgi -c gunicorn.config.py --workers 2 --threads 2 --reload
```
*specifying **DJANGO_SETTINGS_MODULE** is necessary for opentelemetry instrumentation to work*

**For this example, sample command would look like**
```
DJANGO_SETTINGS_MODULE=mysite.settings  OTEL_RESOURCE_ATTRIBUTES=service.name=MainApp OTEL_EXPORTER_OTLP_ENDPOINT="http://<IP Of SigNoz>:4317" opentelemetry-instrument gunicorn mysite.wsgi -c gunicorn.config.py --workers 2 --threads 2 --reload
```
# If want to run docker image of django app directly 
```
docker run --env OTEL_METRICS_EXPORTER=none \
    --env OTEL_SERVICE_NAME=djangoApp \
    --env OTEL_EXPORTER_OTLP_ENDPOINT=host.docker.internal:4317 \
    --env DJANGO_SETTINGS_MODULE=mysite.settings \
    -p 8000:8000 \
    -t signoz/sample-django:latest1 opentelemetry-instrument gunicorn mysite.wsgi -c gunicorn.config.py --workers 2 --threads 2 --reload --bind 0.0.0.0:8000
```

# If want to use docker image of django app in docker-compose
Add below service to your docker-compose
```
  django-app:
    image: "signoz/sample-django:latest"
    container_name: sample-django
    command: opentelemetry-instrument gunicorn mysite.wsgi -c gunicorn.config.py --workers 2 --threads 2 --reload --bind 0.0.0.0:8000
    ports:
      - "8000:8000"
    environment:
    - OTEL_METRICS_EXPORTER=none
    - OTEL_SERVICE_NAME=djangoApp
    - OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317
    - DJANGO_SETTINGS_MODULE=mysite.settings
```

# Browsing the app and checking at SigNoz
1. Visit `http://localhost:8000/admin` and create a question for poll
2. Then visit the list of polls at `http://localhost:8000/polls/` and explore the polls
3. The data should be visible now in SigNoz at `http://<IP of SigNoz>:3000`




