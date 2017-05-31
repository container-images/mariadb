#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# This Modularity Testing Framework helps you to write tests for modules
# Copyright (C) 2017 Red Hat, Inc.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# he Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# Authors: Rado Pitonak <rpitonak@redhat.com>
#

from avocado import main
from avocado.core import exceptions
from moduleframework import module_framework
import time


class SqlQueriesCheck(module_framework.AvocadoTest):
    """
    :avocado: enable
    """

    # prefix for mysql queries from command line
    MYSQL_CMD = 'mysql --host={} -u"$MYSQL_USER" -p"$MYSQL_PASSWORD" "$MYSQL_DATABASE" -e"{}"'

    def testConnectToDB(self):
        """
        Test connection to database
        """

        sql_query = "SELECT 1;"

        self.start()
        # wait for mariadb to start
        time.sleep(15)

        container_ip = self.runHost("docker inspect -f '{{{{range .NetworkSettings.Networks}}}}{{{{.IPAddress}}}}{{{{end}}}}' mariadb_database").stdout

        print "CONTAINER IP ASA:" + container_ip

        # remove end of line character
        container_ip = container_ip[:-1]

        self.run(self.MYSQL_CMD.format(container_ip, sql_query))

    def testCreateTable(self):
        """
        Creation of table in database
        """

        sql_query = "CREATE TABLE my_table(ID INT PRIMARY KEY NOT NULL);"

        self.start()
        # wait for mariadb to start
        time.sleep(15)

        container_ip = self.runHost("docker inspect -f '{{{{range .NetworkSettings.Networks}}}}{{{{.IPAddress}}}}{{{{end}}}}' mariadb_database").stdout

        # remove end of line character
        container_ip = container_ip[:-1]

        self.run(self.MYSQL_CMD.format(container_ip, sql_query))

    def testComplexDB(self):
        """
        Test different requests towards database (create table, insert,select, drop table)
        """

        # sql queries used for this test case
        sql_queries = {'create_table': 'CREATE TABLE my_table(ID INT PRIMARY KEY NOT NULL, NAME VARCHAR(255));',
                       'insert_data': 'INSERT INTO my_table values({}, \'{}\');',
                       'select': 'SELECT name FROM my_table;',
                       'drop': 'DROP TABLE my_table'}

        self.start()
        # wait for mariadb to start
        time.sleep(15)

        container_ip = self.runHost(
            "docker inspect -f '{{{{range .NetworkSettings.Networks}}}}{{{{.IPAddress}}}}{{{{end}}}}' mariadb_database").stdout

        # remove end of line character
        container_ip = container_ip[:-1]

        # creation of table
        self.run(self.MYSQL_CMD.format(container_ip, sql_queries['create_table']))

        # insert data
        self.run(self.MYSQL_CMD.format(container_ip, sql_queries['insert_data'].format(1, 'name1')))
        self.run(self.MYSQL_CMD.format(container_ip, sql_queries['insert_data'].format(2, 'name2')))

        # select query for validating output
        self.run('{} | grep -E "name1|name2"'.format(self.MYSQL_CMD.format(container_ip, sql_queries['select'])))

        # delete table
        self.run(self.MYSQL_CMD.format(container_ip, sql_queries['drop']))


if __name__ == '__main__':
    main()
