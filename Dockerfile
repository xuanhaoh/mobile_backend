FROM python:3.7
WORKDIR /usr/app/
COPY ./* /usr/app/
RUN pip install -r /usr/app/requirements.txt
CMD python app.py
