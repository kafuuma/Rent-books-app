FROM python:3.7

WORKDIR /usr/src/app

# RUN apt-get install libpq-dev

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app
RUN chmod a+x scripts/start.sh && chmod a+x scripts/initdb.sh \
    && chmod a+x scripts/test.sh

CMD ["scripts/start.sh"]
