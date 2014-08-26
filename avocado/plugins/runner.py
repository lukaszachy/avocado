# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
#
# See LICENSE for more details.
#
# Copyright: Red Hat Inc. 2013-2014
# Author: Ruda Moura <rmoura@redhat.com>

"""
Base Test Runner Plugins.
"""

import os

from avocado.plugins import plugin
from avocado.core import data_dir
from avocado.core import output
from avocado.utils import path
from avocado import sysinfo
from avocado import job


class TestLister(plugin.Plugin):

    """
    Implements the avocado 'list' subcommand
    """

    name = 'test_lister'
    enabled = True

    def configure(self, parser):
        """
        Add the subparser for the list action.

        :param parser: Main test runner parser.
        """
        self.parser = parser.subcommands.add_parser(
            'list',
            help='List available test modules')
        super(TestLister, self).configure(self.parser)

    def run(self, args):
        """
        List available test modules.

        :param args: Command line args received from the list subparser.
        """
        bcolors = output.term_support
        pipe = output.get_paginator()
        base_test_dir = data_dir.get_test_dir()
        test_files = os.listdir(base_test_dir)
        test_dirs = []
        blength = 0
        for t in test_files:
            inspector = path.PathInspector(path=t)
            if inspector.is_python():
                clength = len((t.split('.')[0]))
                if clength > blength:
                    blength = clength
                test_dirs.append((t.split('.')[0], os.path.join(base_test_dir, t)))
        format_string = "    %-" + str(blength) + "s %s\n"
        pipe.write(bcolors.header_str('Tests dir: %s\n' % base_test_dir))
        if len(test_dirs) > 0:
            pipe.write(bcolors.header_str(format_string % ('Alias', 'Path')))
            for test_dir in test_dirs:
                pipe.write(format_string % test_dir)
        else:
            pipe.write(bcolors.header_str('No tests were found on current '
                                          'tests dir'))


class TestRunner(plugin.Plugin):

    """
    Implements the avocado 'run' subcommand
    """

    name = 'test_runner'
    enabled = True

    def configure(self, parser):
        """
        Add the subparser for the run action.

        :param parser: Main test runner parser.
        """
        self.parser = parser.subcommands.add_parser(
            'run',
            help='Run a list of test modules or dropin tests (space separated)')

        self.parser.add_argument('url', type=str, default=None,
                                 help=('List of test IDs (aliases or paths)'),
                                 nargs='?')

        self.parser.add_argument('-z', '--archive', action='store_true', default=False,
                                 help='Archive (ZIP) files generated by tests')

        self.parser.add_argument('-m', '--multiplex-file', type=str, default=None,
                                 help=('Path to an avocado multiplex '
                                       '(.mplex) file '),
                                 nargs='?')

        self.parser.add_argument('--keep-tmp-files', action='store_true', default=False,
                                 help='Keep temporary files generated by tests')

        self.parser.add_argument('--unique-id', type=str, default=None,
                                 help=('Unique Job id. Used by a server when job '
                                       'was created at the server and run on a '
                                       'different test machine'))
        super(TestRunner, self).configure(self.parser)

    def run(self, args):
        """
        Run test modules or dropin tests.

        :param args: Command line args received from the run subparser.
        """
        job_instance = job.Job(args)
        rc = job_instance.run()
        if args.url is None:
            self.parser.print_help()
        return rc


class SystemInformation(plugin.Plugin):

    """
    Collect system information
    """

    name = 'sysinfo'
    enabled = True

    def configure(self, parser):
        """
        Add the subparser for the run action.

        :param parser: Main test runner parser.
        """
        self.parser = parser.subcommands.add_parser(
            'sysinfo',
            help='Collect system information')
        self.parser.add_argument('sysinfodir', type=str,
                                 help='Dir where to dump sysinfo',
                                 nargs='?', default='')
        super(SystemInformation, self).configure(self.parser)

    def run(self, args):
        sysinfo.collect_sysinfo(args)
