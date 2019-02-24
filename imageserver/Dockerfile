FROM python:2.7

# Update
RUN pip install --upgrade pip

# dependencies
RUN mkdir -p /srv/ownzones/imageserver
WORKDIR /srv/ownzones

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY gunicorn.conf gunicorn.conf

# sources
# RUN mkdir /home/imageserver
RUN mkdir -p /srv/ownzones/images
RUN mkdir -p /srv/ownzones/cache

COPY src imageserver

EXPOSE  8000
CMD gunicorn --config=gunicorn.conf imageserver.app:app