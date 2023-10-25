FROM python:3.8
RUN apt update
RUN apt install -y socat
RUN mkdir /server
COPY flag.txt /server
COPY public_key.json /server
COPY server.py /server
COPY server.sh /server
COPY graph.py /server
WORKDIR /server
RUN chmod +x /server/server.sh
EXPOSE 3000
CMD /server/server.sh