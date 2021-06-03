# member list for cross-referencing

import csv
import pprint
import os.path

# TODO: generalize MAX_VALID so is_member can be called with a specific value
#MAX_VALID = 2759  # TDW 2020 maximum
MAX_VALID = 2840  # TDW 2021 maximum


def get_memberlist(inputfile):
    """ Helper to create the Ordered Dict of member numbers"""
    memberlist = {}
    with open(inputfile, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            memberlist.setdefault(row['nr'], []).append(row)
    return memberlist


# Member file pulled from hamclubs.info
_dirname = os.path.dirname(__file__)
memberlist = get_memberlist(_dirname + '/podxs070_callsigns.txt')


def is_member(call):
    """
        Walks the list of members to find the 070# that matches the callsign
        This assumes there's a one-to-one mapping, which may not be true (eg,
        SK reassignment), but should be generally ok.  Returns the 070# if found
        otherwise, returns False
    """
    for entry in memberlist:
        if int(entry) <= MAX_VALID:
            for record in memberlist[entry]:
                if call.upper() == record['call'].upper():
                    return entry
    return False


if __name__ == '__main__':
    dirname = os.path.dirname(__file__)
    memberlist = get_memberlist(dirname + '/podxs070_callsigns.txt')
    pprint.pprint(memberlist)
