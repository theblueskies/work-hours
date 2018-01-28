FROM python:3

RUN mkdir -p /src/wave
WORKDIR /src
ADD . /src

RUN pip install -r /src/requirements.txt
EXPOSE 8000

RUN python /src/manage.py migrate

CMD ["python", "/src/manage.py", "runserver", "0.0.0.0:8000"]
