FROM nginx
RUN apt-get update
RUN apt-get install -y git
RUN git clone https://github.com/chrisparnin/checkbox.io
RUN mkdir /etc/nginx/sites-available
COPY default /etc/nginx/sites-available/default
RUN cp checkbox.io/local-conf/nginx.conf /etc/nginx/nginx.conf
RUN /etc/init.d/nginx restart