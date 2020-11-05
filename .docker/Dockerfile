FROM python:3.8.5-slim-buster
LABEL maintainer="Cornershop SRE"

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    # some Python modules come from git
    git openssh-client

RUN groupadd -g 1337 cornershop && \
    useradd -m -d /opt/cornershop -u 1337 -g cornershop cornershop

USER cornershop
ENV PATH /opt/cornershop/.local/bin:$PATH

ADD --chown=cornershop:cornershop .docker/gunicorn_config.py /
ADD --chown=cornershop:cornershop requirements.txt /requirements.txt
RUN pip install --no-warn-script-location --disable-pip-version-check --no-cache-dir --src=/opt/cornershop/src --user --upgrade -r /requirements.txt

COPY --chown=cornershop:cornershop ./src/ /opt/cornershop/api/
WORKDIR /opt/cornershop/api

EXPOSE 8000
CMD ["gunicorn", "--config=/gunicorn_config.py", "wsgi:app"]
