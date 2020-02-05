FROM python:3.7

RUN pip install gunicorn

COPY . /app

RUN pip install -r /app/requirements.txt

WORKDIR /app/kbsbot/telegramchannel

ENV BASE_URL="127.0.0.1:5005"
ENV CONNECTION_KEY="tokendeseguridad"
ENV API_KEY="616944972:AAFUU_Od5-fiEg_Oe7pV0g-aWgXuAVM0ctk"

CMD ["python", "/app/kbsbot/telegramchannel/launch.py"]


