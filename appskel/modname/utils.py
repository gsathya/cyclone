# coding: utf-8
#
# Copyright 2012 Alexandre Fiori
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

import cyclone.escape
import cyclone.redis
import cyclone.sqlite
import cyclone.web

from twisted.enterprise import adbapi


class BaseHandler(cyclone.web.RequestHandler):
    #def get_current_user(self):
    #    user_json = self.get_secure_cookie("user")
    #    if user_json:
    #        return cyclone.escape.json_decode(user_json)

    def get_user_locale(self):
        lang = self.get_secure_cookie("lang")
        if lang:
            return cyclone.locale.get(lang)


class DatabaseMixin(object):
    mysql = None
    redis = None
    sqlite = None

    @classmethod
    def setup(self, settings):
        conf = settings.get("sqlite_settings")
        if conf:
            DatabaseMixin.sqlite = cyclone.sqlite.InlineSQLite(conf.database)

        conf = settings.get("redis_settings")
        if conf:
            DatabaseMixin.redis = cyclone.redis.lazyConnectionPool(
                            conf.host, conf.port, conf.dbid, conf.poolsize)

        conf = settings.get("mysql_settings")
        if conf:
            DatabaseMixin.mysql = adbapi.ConnectionPool("MySQLdb",
                            host=conf.host, port=conf.port, db=conf.database,
                            user=conf.username, passwd=conf.password,
                            cp_min=1, cp_max=conf.poolsize,
                            cp_reconnect=True, cp_noisy=conf.debug)
