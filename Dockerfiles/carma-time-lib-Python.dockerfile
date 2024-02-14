FROM "ghcr.io/usdot-fhwa-stol/carma-builds-x64:latest" as build
RUN mkdir /workspaces
RUN cd /workspaces
RUN mkdir /carma-time-lib
COPY . /workspaces/carma-time-lib


ARG CMAKE_VERSION=3.25.1
ARG NUM_JOBS=8


ENV DEBIAN_FRONTEND noninteractive

# Install package dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        software-properties-common \
        autoconf \
        automake \
        libtool \
        pkg-config \
        ca-certificates \
        libssl-dev \
        wget \
        git \
        curl \
        language-pack-en \
        locales \
        locales-all \
        vim \
        gdb \
        valgrind && \
    apt-get clean

# System locale
# Important for UTF-8
ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

# Install CMake
RUN cd /tmp && \
    wget https://github.com/Kitware/CMake/releases/download/v${CMAKE_VERSION}/cmake-${CMAKE_VERSION}.tar.gz && \
    tar xzf cmake-${CMAKE_VERSION}.tar.gz && \
    cd cmake-${CMAKE_VERSION} && \
    ./bootstrap && \
    make -j${NUM_JOBS} && \
    make install && \
    rm -rf /tmp/*

WORKDIR /workspaces/carma-time-lib
RUN apt install libboost-python-dev
# RUN cmake .



# FROM python:3
# COPY --from=build /workspaces/carma-time-lib . 
# RUN pip install --no-cache-dir --upgrade pip 

# Install Boost
# https://www.boost.org/doc/libs/1_80_0/more/getting_started/unix-variants.html

# RUN apt-get update
# RUN apt-get install python3-dev -y
# RUN cd /tmp 
# RUN wget https://boostorg.jfrog.io/artifactory/main/release/1.82.0/source/boost_1_82_0.tar.bz2
# RUN tar --bzip2 -xf boost_1_82_0.tar.bz2 


# RUN cd boost_1_82_0
# WORKDIR boost_1_82_0
# RUN ./bootstrap.sh --prefix=/usr/
# RUN ./b2 install --with-python
# RUN ./b2 install
# CMD ["echo", "Hello!"]
# RUN rm -rf /tmp/*
# WORKDIR /
