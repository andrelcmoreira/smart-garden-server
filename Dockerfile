FROM python:3.8

ARG SECRET_KEY
ENV SECRET_KEY=${SECRET_KEY}

EXPOSE 5000

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt

WORKDIR /app
ENTRYPOINT ["python3", "app/run.py"]
