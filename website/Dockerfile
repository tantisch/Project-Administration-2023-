FROM python:3.8

WORKDIR /website

RUN pip install -U pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --dev --deploy --system

COPY . .

EXPOSE 5000
ENTRYPOINT ["python", "./wsgi.py"]
