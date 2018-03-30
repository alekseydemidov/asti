FROM docker.io/jenkins 

# Update jenkins to last version
ADD --chown=jenkins:jenkins http://updates.jenkins-ci.org/latest/jenkins.war /usr/share/jenkins/jenkins.war
#COPY ./jenkins.war /usr/share/jenkins/jenkins.war

# Configure jenkins and create admin
#COPY --chown=jenkins:jenkins templates /var/jenkins_home

ENV JAVA_OPTS -Djava.awt.headless=true -Dhudson.model.DirectoryBrowserSupport.CSP=false
RUN /usr/local/bin/install-plugins.sh ssh-slaves robot locale git jdk-tool
