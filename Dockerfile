FROM python:3.8-slim-buster
ENV TEMP_DIR = '/app/.sys-cache'

RUN apt update
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 80
CMD [ "uvicorn", "main:app","--host","0.0.0.0", "--port", "80"]
