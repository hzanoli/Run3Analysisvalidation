FROM centos:7

SHELL ["/bin/bash", "-c"]

# Install ROOT
RUN yum install -y epel-release \
    && yum install -y \
    python3 \
    python3-root \
    root \
    && yum clean all \
    && rm -rf /var/cache/yum

COPY requirements.txt /requirements/requirements.txt

RUN pip3 install -r /requirements/requirements.txt

COPY . /o2qaplots
RUN pip3 install -e /o2qaplots/. --no-cache-dir
