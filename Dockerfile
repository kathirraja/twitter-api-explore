FROM python:alpine3.10

ENV PATH="/scripts:${PATH}"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./pip_rec.txt /pip_rec.txt
RUN pip install --upgrade pip
RUN pip install -r /pip_rec.txt


RUN adduser --disabled-password appadmin
RUN mkdir -p /home/appadmin/django_twitter
RUN mkdir -p /vol/web/
RUN chown -R appadmin:appadmin /home/appadmin/django_twitter
RUN chown -R appadmin:appadmin /vol/web/
USER appadmin

COPY ./django_twitter /home/appadmin/django_twitter
WORKDIR /home/appadmin/django_twitter

USER root
RUN mkdir /scripts
COPY ./scripts /scripts
RUN chmod +x /scripts/*

USER appadmin
CMD ["twitter_stater.sh"]
