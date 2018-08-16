from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.errors import AnsibleError, AnsibleFilterError
from operator import itemgetter

def sort_multi(data, *args):
    ''' sort list using multiple attributes
    '''
    return sorted(data, key = itemgetter(*args))

def keyvalue_dict(data):
    result = {}
    for item in data:
        if item["key"]:
            result[item["key"]] = item["value"]
    return result

def single_quote(string):
    return "'" + string + "'"

class FilterModule(object):
    ''' Query filter '''

    def filters(self):
        return {
            'sort_multi': sort_multi,
            'keyvalue_dict': keyvalue_dict,
            'single_quote': single_quote
        }
