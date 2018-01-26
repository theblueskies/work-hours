FROM python:3

RUN mkdir src
WORKDIR src
ADD . src

RUN pip install -r src/requirements.txt
EXPOSE 80

CMD ['python', 'manage.py', 'runserver']
