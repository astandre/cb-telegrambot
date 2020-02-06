FROM python:3.7

COPY . /app

RUN pip install -r /app/requirements.txt
RUN pip install /app/

#WORKDIR /app/kbsbot/telegramchannel

#ENV  BASE_URL="127.0.0.1:5005"
ENV  BASE_URL="http://172.28.1.2:8005"
ENV  CONNECTION_KEY="tokendeseguridad"
ENV  API_KEY="616944972:AAFUU_Od5-fiEg_Oe7pV0g-aWgXuAVM0ctk"

CMD ["telegram-channel"]


