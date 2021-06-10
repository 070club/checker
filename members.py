# member list for cross-referencing

import csv
import pprint
import os.path
import collections


def get_memberlist(inputfile):
    """ Helper to create the Ordered Dict of member numbers"""
    memberlist = collections.OrderedDict()
    with open(inputfile, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            memberlist.setdefault(row['nr'], []).append(row)
    return memberlist


# Member file pulled from hamclubs.info
_dirname = os.path.dirname(__file__)
memberlist = get_memberlist(_dirname + '/podxs070_callsigns.txt')


def is_member(call, max_valid=None):
    """
        Walks the list of members to find the 070# that matches the callsign
        This assumes there's a one-to-one mapping, which may not be true (eg,
        SK reassignment), but should be generally ok.  Returns the 070# if found
        otherwise, returns False
    """

    splitcall = call.split('/')

    if max_valid is None:
        last_entry = next(reversed(memberlist))
    else:
        last_entry = max_valid

    for entry in memberlist:
        if int(entry) <= int(last_entry):
            for record in memberlist[entry]:
                if len(splitcall) == 1:
                    if call.upper() == record['call'].upper():
                        return entry
                else:
                    for item in splitcall:
                        if item.upper() == record['call'].upper():
                            return entry
    return False


if __name__ == '__main__':
    dirname = os.path.dirname(__file__)
    memberlist = get_memberlist(dirname + '/podxs070_callsigns.txt')
    pprint.pprint(memberlist)
