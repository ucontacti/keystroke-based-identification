FROM python:3.7

LABEL Author="Saleh Daghigh"
LABEL E-mail="ucontacti2012@gmail.com"

WORKDIR /app

COPY . /app

ADD app.py /

RUN pip install -r requirements.txt

EXPOSE 5000

CMD [ "python", "./app.py" ]
