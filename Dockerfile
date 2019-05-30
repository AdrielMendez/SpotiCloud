FROM python:3
EXPOSE 80
WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN mkdir result
COPY . .

CMD [ "python", "run.py" ]
