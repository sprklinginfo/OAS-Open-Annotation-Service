## begin license ##
# 
# "Open Annotation Service" enables exchange, storage and search of
# heterogeneous annotations using a uniform format (Open Annotation format) and
# a uniform web service interface. 
# 
# Copyright (C) 2012 Meertens Instituut (KNAW) http://meertens.knaw.nl
# Copyright (C) 2012 Seecr (Seek You Too B.V.) http://seecr.nl
# 
# This file is part of "Open Annotation Service"
# 
# "Open Annotation Service" is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# "Open Annotation Service" is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with "Open Annotation Service"; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
# 
## end license ##

from environment import Environment

from os.path import join
from urlparse import urlsplit
from lxml.etree import parse

from meresco.core import Observable
from meresco.components import readConfig
from weightless.core import compose, be

from oas.harvester import Harvest, SruUpload

def process(config):
    env = Environment(root=join(config['databasePath'], 'harvester'))
    for repository in env.getRepositories():
        if not repository.active:
            continue
        dna = be(
            (Observable(),
                (Harvest(),
                    (SruUpload(
                        hostname=config['hostName'], 
                        portnumber=int(config['portNumber']), 
                        path=config['sru.updatePath'], 
                        apiKey=repository.apiKey),)
                    )
                )
            )
        list(compose(dna.all.process(repository=repository)))

def main(configFile):
    process(config=readConfig(configFile))
