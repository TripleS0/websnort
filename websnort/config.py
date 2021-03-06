# Websnort - Web service for analysing pcap files with snort
# Copyright (C) 2013-2015 Steve Henderson
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import
from __future__ import unicode_literals

try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser

import os
from pkg_resources import DistributionNotFound, Requirement, ResourceManager

# user home path
USER_PATH = os.path.expanduser("~/.websnort")
# system path
SYSTEM_PATH = "/etc/websnort"
# path to conf files if package not installed
SOURCE_PATH = os.path.join(os.path.dirname(__file__), 'conf')

def installed_location(filename):
    """
    Returns the full path for the given installed file or None if not found.

    :param filename: The filename to search for.
    :returns: The absolute filepath for the file or None if not installed.
    """
    try:
        return ResourceManager().resource_filename(Requirement.parse("websnort"), filename)
    except DistributionNotFound:
        return None

class Config:
    def __init__(self, cfg='websnort.conf'):
        """
        Main config file parser for websnort.
        Will search the following locations for the given config, 
        in precedence order:
        * ~/.websnort/
        * /etc/websnort
        * <package_install_location>
        * <relative_to_source>

        :param cfg: Config filename to parse.
        """
        installed_path = installed_location('conf/' + cfg) or 'notfound'
        parser = ConfigParser()
        parser.read([os.path.join(SOURCE_PATH, cfg),
                     installed_path,
                     os.path.join(SYSTEM_PATH, cfg),
                     os.path.join(USER_PATH, cfg),
                     cfg])

        self.modules = {}
        for x in parser.get('websnort', 'ids').split(','):
            x = x.strip()
            options = {'name': x}
            for y in parser.options(x):
                options[y] = parser.get(x, y)
            self.modules[x] = options
