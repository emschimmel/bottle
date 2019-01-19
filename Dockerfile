FROM python:3

ADD index.py /
ADD actions /actions
ADD config /config
ADD img /img
ADD model /model
ADD scrapper /scrapper
ADD static /static
ADD views /views
ADD requirements.txt /requirements.txt

RUN pip install -r requirements.txt

CMD [ "python", "./index.py" ]