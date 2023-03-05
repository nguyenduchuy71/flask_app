FROM python:3.7-alpine

WORKDIR /app

COPY . .

RUN python3 -m pip install --upgrade pip

RUN pip install -r requirements.txt

ENV PORT 5555

EXPOSE 5555

CMD ["python", "server.py"]
