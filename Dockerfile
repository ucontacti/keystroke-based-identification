FROM alpine:latest

LABEL Author="Saleh Daghigh"
LABEL E-mail="ucontacti2012@gmail.com"

RUN apk add  python3-dev \
    && pip3 install --upgrade pip

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]
