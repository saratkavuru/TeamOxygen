# sudo docker build . -t some-content-nginx7
# sudo docker tag some-content-nginx7 agoel5/some-content-nginx7
# sudo docker push agoel5/some-content-nginx7
# sudo docker run --name some-content-nginx7 -d some-content-nginx7 
# sudo docker top some-content-nginx7
# sudo docker exec -it some-content-nginx7 /bin/bash
FROM nginx
RUN apt-get update
RUN apt-get install -y git curl
RUN git clone https://github.com/chrisparnin/checkbox.io
RUN mkdir /etc/nginx/sites-available
COPY default /etc/nginx/sites-available/default
RUN cp checkbox.io/local-conf/nginx.conf /etc/nginx/nginx.conf
RUN apt-get install -my wget gnupg
RUN curl -sL https://deb.nodesource.com/setup_9.x | bash
RUN apt-get update
RUN apt-get install --yes nodejs build-essential
RUN npm install -g forever
RUN cd checkbox.io/server-side/site && npm install
ENTRYPOINT /etc/init.d/nginx start && cd checkbox.io/server-side/site && MONGO_USER=admin MONGO_PASSWORD=password MONGO_PORT=3002 MONGO_IP=mongo MAIL_USER=admin MAIL_PASSWORD=password MAIL_SMTP=smtp.gmail.com node server.js