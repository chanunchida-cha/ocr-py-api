FROM python:3.10

WORKDIR /src

ADD ./ /src

RUN pip install --upgrade pip
RUN apt update; apt install -y libgl1
RUN apt-get update \
  && apt-get -y install tesseract-ocr
RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 8000 

CMD ["python", "main.py"]