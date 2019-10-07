FROM python:3.7
ADD . /code
WORKDIR /code
# install dependencies
RUN pip install -r requirements.txt
CMD python app.py