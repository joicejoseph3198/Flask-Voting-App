FROM python:3.8.10-slim
WORKDIR /app
ADD . .
RUN pip install -r requirements.txt
CMD python3 run.py
