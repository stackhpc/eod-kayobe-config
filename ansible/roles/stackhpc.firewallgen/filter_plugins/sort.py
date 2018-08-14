from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleError, AnsibleFilterError
from operator import itemgetter

def sort_multi(data, *args):
    ''' sort list using multiple attributes
    '''
    return sorted(data, key = itemgetter(*args))

class FilterModule(object):
    ''' Query filter '''

    def filters(self):
        return {
            'sort_multi': sort_multi
        }
