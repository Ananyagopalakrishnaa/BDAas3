# Use the official Ubuntu base image
FROM ubuntu:latest

# Install required packages
RUN apt-get update && \
    apt-get install -y wget openjdk-11-jdk python3 python3-pip && \
    apt-get clean

# Install Python packages
RUN pip3 install praw confluent-kafka newsapi-python

# Set up environment variables
ENV KAFKA_HOME=/opt/kafka
ENV ZOOKEEPER_HOME=/opt/zookeeper
ENV PATH=${KAFKA_HOME}/bin:${ZOOKEEPER_HOME}/bin:${PATH}

# Copy server.properties and zookeeper.properties
COPY server.properties /opt/kafka/config/server.properties
COPY zookeeper.properties /opt/zookeeper/conf/zookeeper.properties

# Copy Python script
COPY streamTopic1.py /app/streamTopic1.py

# Set working directory
WORKDIR /app

# Command to run Python script
CMD ["python3", "streamTopic1.py"]
