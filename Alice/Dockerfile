FROM python:3.8
RUN apt update
RUN apt install -y socat
RUN mkdir /server
COPY graph.py /server
COPY private_key.json /server
COPY alice.py /server
COPY server.sh /server
WORKDIR /server
RUN chmod +x /server/server.sh
EXPOSE 3000
CMD /server/server.sh