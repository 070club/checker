#!/usr/local/bin/python3
#
# membership.py
#
# module for validating membership submissions

import sys

def test_record(entry, conditions, valid_records):
    # Walk through each adif entry and validate against a bunch of stuff

    errors = ['not_valid_band', 'is_not_psk', 'is_dupe']

    if contests.rec_in_bands(entry, conditions['valid_bands'], None):
        errors.remove('not_valid_band')

    if contests.rec_is_psk(entry, conditions['valid_modes'], None):
        errors.remove('is_not_psk')

    if contests.rec_is_not_dupe(entry, valid_records):
        errors.remove('is_dupe')

    if len(errors) == 0:
        return True, None
    else:
        return False, errors


def qso_validate(adif_files):
    conditions = { 'valid_modes': ['psk', 'bpsk',
                                  'psk31', 'bpsk31', 'qpsk31',
                                  ],
                    'valid_bands': ['6m', '10m', '15m', '20m', '40m', '80m', '160m'],
                   }
    valid_records = []
    invalid_records = []
    # loop through adif files
    # for each adif file, grab summary info
    for entry in adif_files:
        for record in adif_files[entry]:
            s_record = contests.synthesize_fields(record)
            status, errors = test_record(s_record, conditions, valid_records)
            if errors:
                invalid_records.append({'data': s_record, 'errors': errors})
            else:
                valid_records.append(s_record)
    return valid_records, invalid_records


if __name__ == '__main__':
    import adifparser
    import contests
    import argparse
    import pprint
    import os.path

    parser = argparse.ArgumentParser(description='Membership validator')
    parser.add_argument('--call', metavar='CALL')
    parser.add_argument('--adif', metavar='ADIF', nargs='*')
    parser.add_argument('--debug', dest='debug', action='store_true')
    parser.set_defaults(debug=False)
    args = parser.parse_args()

    adif_files = {}
    for adif in args.adif:
        try:
            rootname, ext = os.path.splitext(adif)
        except FileNotFoundError:
            print('File {} not found; skipping'.format(adif), file=sys.stderr)
        else:
            name = os.path.basename(rootname)
            adif_files[name] = adifparser.parse(adif)

    if len(adif_files) == 0:
        print("No files found: Exiting", file=sys.stderr)
        exit(1)

    valid_entries = None
    invalid_entries = None
    valid_entries, invalid_entries = qso_validate(adif_files)

    if args.debug:
        pprint.pprint(valid_entries)
        pprint.pprint(invalid_entries)

    if valid_entries:
        print('\nMembership application for: {}'.format(args.call.upper()))
        print('Number of Valid QSOs: {}'.format(len(valid_entries)))
        contests.print_entries(valid_entries, valid=True)
    if invalid_entries:
        contests.print_entries(invalid_entries, valid=False)
