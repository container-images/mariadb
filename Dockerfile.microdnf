FROM baseruntime/baseruntime:latest

ENV NAME=mariadb \
    ARCH=x86_64 \
    VERSION=0 \
    RELEASE=1 \
    MARIADB_VERSION="10.1.21" \
    HOME=/var/lib/mysql \
    SUMMARY="MariaDB 10.1 SQL database server" \
    DESCRIPTION="MariaDB is a multi-user, multi-threaded SQL database server. The container \
image provides a containerized packaging of the MariaDB mysqld daemon and client application. \
The mysqld server daemon accepts connections from clients and provides access to content from \
MariaDB databases on behalf of the clients."

LABEL MAINTAINER "Matus Kocka" <mkocka@redhat.com>
LABEL summary="MariaDB is a multi-user, multi-threaded SQL database server" \
      name="$FGC/$NAME" \
      version="$VERSION" \
      release="$RELEASE.$DISTTAG" \
      architecture="$ARCH" \
      description="MariaDB is a multi-user, multi-threaded SQL database server." \
      vendor="Fedora Project" \
      com.redhat.component="$NAME" \
      usage="docker run -e MYSQL_USER=<user_name> -e MYSQL_PASSWORD=<password> -e MYSQL_DATABASE=<db_name> -e MYSQL_ROOT_PASSWORD=<root_password> -p 3306:3306 mariadb" \
      org.fedoraproject.component="mariadb" \
      authoritative-source-url="registry.fedoraproject.org" \
      io.k8s.description="MariaDB is a multi-user, multi-threaded SQL database server" \
      io.k8s.display-name="MariaDB 10.1" \
      io.openshift.expose-services="3306:mysql" \
      io.openshift.tags="database,mysql,mariadb,mariadb101,galera" 

RUN INSTALL_PKGS="rsync tar gettext hostname bind-utils python3 policycoreutils" && \
    microdnf --nodocs install mariadb mariadb-server -y && \
    microdnf --nodocs install $INSTALL_PKGS -y && \
    microdnf clean all && \
    mkdir -p /var/lib/mysql/data && chown -R mysql.0 /var/lib/mysql && \
    test "$(id mysql)" = "uid=27(mysql) gid=27(mysql) groups=27(mysql)"

ENV CONTAINER_SCRIPTS_PATH=/usr/share/container-scripts/mysql \
    MYSQL_PREFIX=/usr

EXPOSE 3306

COPY root /

RUN rm -rf /etc/my.cnf.d/*

RUN /usr/libexec/container-setup

VOLUME ["/var/lib/mysql/data"]

USER 27

ENTRYPOINT ["container-entrypoint"]

CMD ["run-mysqld"]
