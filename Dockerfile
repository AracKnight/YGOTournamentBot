FROM python:3.7.0-slim as build
RUN apt-get update && apt-get install gcc -y && apt-get clean
COPY . /bot
WORKDIR /bot
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirement.txt
RUN apt-get autoremove

FROM build

CMD [ "python","main.py" ]
