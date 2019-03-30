#  Copyright 2013-2014 Nokia Solutions and Networks
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
from optparse import OptionParser
from os.path import exists


DEFAULT_DB_NAME = 'robot_results'

class ReaderOptions(object):

    def __init__(self):
        self._parser = OptionParser()
        self._add_parser_options()
        self._options, self._files = self._get_validated_options()

    def _add_parser_options(self):
        options = [
            ('-d', '--dry-run', {'action': 'store_true',
                                 'default': False,
                                 'dest': 'dry_run',
                                 'help': 'do everything except store results into disk'}),

            ('-H', '--host', {'dest': 'db_host',
                              'default': 'localhost',
                              'help': 'host where Mysql is running'}),

            ('-u', '--user', {'dest': 'db_user',
                              'default': 'root',
                              'help': 'username to connect to Mysql'}),

            ('-p', '--password', {'dest': 'db_passwd',
                                  'default': '',
                                  'help': 'password to connect to Mysql'}),

            ('-k', '--also-keywords', {'action':'store_true',
                                       'default': False,
                                       'dest': 'include_keywords',
                                       'help': 'parse also suites\' and tests\' keywords'}),

            ('-v', '--verbose', {'action': 'store_true',
                                 'default': False,
                                 'dest': 'be_verbose',
                                 'help': 'be verbose about the operation'}),

            ('-b', '--database', {'dest': 'db_name',
                                  'default': DEFAULT_DB_NAME,
                                  'help': 'name of the MySQL database for test run results'})
        ]
        for option in options:
            self._parser.add_option(option[0], option[1], **option[2])

    def _get_validated_options(self):
        options, files = self._parser.parse_args()
        self._check_files(files)
        return options, files

    def _check_files(self, files):
        if not files or len(files) < 1:
            self._parser.error('at least one input file is required')
        for file_path in files:
            if not exists(file_path):
                self._parser.error('file "%s" does not exist' % file_path)

    def _exit_with_help(self):
        self._parser.print_help()
        exit(1)

    @property
    def db_host(self):
        return self._options.db_host

    @property
    def db_user(self):
        return self._options.db_user

    @property
    def db_passwd(self):
        return self._options.db_passwd

    @property
    def db_name(self):
        return self._options.db_name

    @property
    def be_verbose(self):
        return self._options.be_verbose

    @property
    def file_paths(self):
        return self._files

    @property
    def dry_run(self):
        return self._options.dry_run

    @property
    def include_keywords(self):
        return self._options.include_keywords
