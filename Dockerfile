FROM fedora:25

MAINTAINER "Matus Kocka" <mkocka@redhat.com>

# MariaDB standalone image for Fedora 26
# Based on work by Honza Horak 
# This image is based on MariaDB image for OpenShift 

ENV MYSQL_VERSION=10.1 \
    HOME=/var/lib/mysql

ENV NAME=mariadb VERSION=10.1 RELEASE=1 ARCH=x86_64
LABEL BZComponent="$NAME" \
        Name="$FGC/$NAME" \
        Version="$VERSION" \
        Release="$RELEASE.$DISTTAG" \
        Architecture="$ARCH"

EXPOSE 3306

RUN INSTALL_PKGS="rsync tar gettext hostname bind-utils mariadb-server policycoreutils" && \
    dnf install -y --setopt=tsflags=nodocs $INSTALL_PKGS && \
    rpm -V $INSTALL_PKGS && \
    dnf clean all && \
    mkdir -p /var/lib/mysql/data && chown -R mysql.0 /var/lib/mysql && \
    test "$(id mysql)" = "uid=27(mysql) gid=27(mysql) groups=27(mysql)"

RUN ln -s /usr/bin/python3 /usr/bin/python

ENV CONTAINER_SCRIPTS_PATH=/usr/share/container-scripts/mysql \
    MYSQL_PREFIX=/usr

ADD files /

RUN rm -rf /etc/my.cnf.d/*
RUN /usr/libexec/container-setup

VOLUME ["/var/lib/mysql/data"]

USER 27

ENTRYPOINT ["container-entrypoint"]
CMD ["run-mysqld"]
