from __future__ import (absolute_import, division, print_function)

from ansible.plugins.lookup import LookupBase
from __main__ import cli


class LookupModule(LookupBase):

    def run(self, terms='', **kwargs):
        return str(cli.options.tags).split(',')
