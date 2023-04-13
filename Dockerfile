FROM python:3.11.0

WORKDIR /Project-Administration-2023-

RUN pip install -U pipenv

COPY Pipfile .
COPY Pipfile.lock .

RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy --system

COPY ./ .

EXPOSE 5000
ENTRYPOINT ["python", "./wsgi.py"]
