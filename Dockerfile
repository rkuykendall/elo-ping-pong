FROM python:2-alpine
ENV PYTHONUNBUFFERED=0

RUN apk add --no-cache gcc \
                       musl-dev \
                       postgresql-dev

ADD requirements.txt /
RUN pip install -r requirements.txt

ADD . /

ADD web.py /
CMD [ "python", "./web.py" ]
