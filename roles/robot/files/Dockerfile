FROM docker.io/alpine
RUN apk update && apk upgrade && apk add --no-cache --update python python-dev py-pip openjdk8-jre-base openssh libffi-dev gcc musl-dev openssl-dev make libxml2-dev libxslt-dev
RUN ssh-keygen -f /etc/ssh/ssh_host_rsa_key -N '' -t rsa && ssh-keygen -f /etc/ssh/ssh_host_dsa_key -N '' -t dsa && ssh-keygen -f /etc/ssh/ssh_host_ecdsa_key -N '' -t ecdsa && ssh-keygen -f /etc/ssh/ssh_host_ed25519_key -N '' -t ed25519 
COPY .ssh /root/.ssh
RUN pip install --upgrade pip ;pip install robotframework robotframework-sshlibrary pyyaml lxml
#RUN pip install robotframework 
EXPOSE 22
ENTRYPOINT ["/usr/sbin/sshd","-D"]

