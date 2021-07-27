FROM python:3.10-rc-buster
RUN mkdir /work
WORKDIR /work
COPY main.py /work
COPY requirements.txt /work
RUN pip install -r requirements.txt

CMD [ "python", "main.py"]
