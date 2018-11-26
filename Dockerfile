FROM python:3.6
COPY . /appserver
WORKDIR /appserver
EXPOSE 5000
RUN pip3 install -r requirements.txt
ENV FLASK_ENV=development
CMD ["flask", "run"]
