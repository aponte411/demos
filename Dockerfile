FROM python:3.7

COPY /requirements.txt /root/requirements.txt
RUN pip install -r /root/requirements.txt

COPY . /root

WORKDIR /root

CMD PYTHONPATH=. python bin/kfserver.py
