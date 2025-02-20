##
#
# Copyright (c) 2025, Lorenzo Pouw.
# All rights reserved.
#
##

FROM python:3.13-slim

WORKDIR /app

RUN pip install --upgrade pip
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ .

CMD ["python", "main.py"]
