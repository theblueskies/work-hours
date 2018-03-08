FROM python:3

RUN mkdir -p /src/wave
WORKDIR /src
ADD . /src

RUN pip install -r /src/requirements.txt

# create unprivileged user
RUN adduser --disabled-password --gecos '' user

EXPOSE 8000

# CMD ["python", "/src/manage.py", "runserver", "0.0.0.0:8000"]
