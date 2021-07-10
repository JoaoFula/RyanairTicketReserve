FROM python:3.8

ENV DISPLAY=:4444

#settup to run python app
COPY . /RYANAIRTICKETRESERVE

WORKDIR /RYANAIRTICKETRESERVE

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD ["python", "./main.py"]