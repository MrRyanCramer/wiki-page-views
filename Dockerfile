FROM python:3.12-alpine

WORKDIR /home/views

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY app app


EXPOSE 5000
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]