# get libs
# get ubuntu image
FROM ubuntu:latest as build
WORKDIR /root/
ENV DEBIAN_FRONTEND=noninteractive

# get leveldb 
RUN apt update -y && \
    apt upgrade -y && \
    apt install git -y && \
    apt install zip -yq && \
    apt install wget -yq && \
    apt install openjdk-8-jdk -y && \
    apt install libleveldb-java libleveldb-api-java -y

# get sbt for build lunesnode
RUN wget https://github.com/sbt/sbt/releases/download/v1.5.5/sbt-1.5.5.zip && \
    unzip sbt*.zip && \
    mv sbt/bin/sbt /usr/bin/sbt && \
    rm -rf sbt*

# get and build lunesnode from github
RUN git clone -b DEX https://github.com/lunes-platform/lunesnode.git lunesnode && \
    mv lunesnode/* . && \
    rm -rf lunesnode/
RUN sbt assembly

# copy files to unpack
RUN cp target/lunesnode-latest.jar /home/
WORKDIR /home/


# unpack lunesnode and save MANIFEST
RUN jar -xvf lunesnode-latest.jar && \
    cp META-INF/MANIFEST.MF .

# remove leveldb old and unpack new leveldb
RUN find . -name *leveldb* -exec rm -rv {} + && \
    cp /usr/share/java/leveldb-api.jar . && \
    cp /usr/share/java/leveldb.jar . && \
    jar -xvf leveldb-api.jar && \
    jar -xvf leveldb.jar  && \
    rm -f *.jar

# pack lunesnode with the new leveldb
RUN cp MANIFEST.MF META-INF/ && \
    jar -cfm lunesnode-latest.jar META-INF/MANIFEST.MF *

COPY ./lunesnode.conf .

FROM ubuntu:latest
WORKDIR /home/
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update -y && apt install openjdk-8-jdk -y

# lunesnode blockchain api
EXPOSE 5555
# lunesnode exchange api
EXPOSE 4444

# copy lunesnode-latest.jar and lunesnode.conf
COPY --from=build /home/lunesnode-latest.jar .
COPY ./lunesnode.conf .

CMD ["java", "-jar", "lunesnode-latest.jar", "lunesnode.conf"]
