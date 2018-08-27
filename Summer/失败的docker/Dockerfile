FROM python:alpine
LABEL maintainer = "tuzhipeng"
RUN pip install flask pymongo bs4  selenium==2.48.0
RUN wget https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
RUN tar xvjf phantomjs-2.1.1-linux-x86_64.tar.bz2 -C /usr/local/share/
RUN ln -sf /usr/local/share/phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/local/bin

RUN apk update

RUN apk add mongodb
RUN mkdir -p /data/db

COPY src /src/
RUN chmod u+x /src/start.sh

EXPOSE 5000
CMD /src/start.sh
