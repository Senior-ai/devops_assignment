# Use an Ubuntu base image
FROM ubuntu:latest

# Install dependencies
RUN apt-get update && \
    apt-get install -y build-essential libpcre3 libpcre3-dev zlib1g zlib1g-dev openssl libssl-dev wget git

# Download Nginx
RUN wget http://nginx.org/download/nginx-1.24.0.tar.gz && \
    tar -xvf nginx-1.24.0.tar.gz

# Clone the Sticky Module from GitHub
RUN git clone https://github.com/liberatti/nginx-sticky-module-ng.git

# Compile Nginx with the Sticky Module
RUN cd nginx-1.24.0 && \
    ./configure --add-module=../nginx-sticky-module-ng && \
    make && \
    make install

RUN apt install curl -y

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY nginx.conf /usr/local/nginx/conf/nginx.conf
# Expose port 80
EXPOSE 80

# Start Nginx when the container launches
CMD ["/usr/local/nginx/sbin/nginx", "-g", "daemon off;"]
