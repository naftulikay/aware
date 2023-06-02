FROM python:3.11-alpine

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

# install dependent libraries
ADD requirements.txt ./
RUN pip install -r requirements.txt

# add source code
ADD app.py ./

# apparently this instruments flask?
RUN opentelemetry-bootstrap -a install

# by default, we will use opentelemetry-instrument as an entrypoint
ENTRYPOINT ["opentelemetry-instrument"]

# and we will pass `flask run -p 8080` to it, which it will execute
CMD ["flask", "run", "-p", "8080"]