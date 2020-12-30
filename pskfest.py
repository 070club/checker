#!/usr/local/bin/python3
#
# pskfest.py
#
# module for calculating pskfest results
#
# TODO: properly handle multiple files at the same time
# TODO: add ability to match logs (check logs)
import sys
import adifparser
import contests
import argparse
import pprint
import os.path
import datetime

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Contests Checker')
    parser.add_argument('--year', metavar='YEAR')
    parser.add_argument('--summary', metavar='SUMMARY')
    parser.add_argument('--delim', metavar='DELIMITER', default=',')
    parser.add_argument('--call', metavar='CALL')
    parser.add_argument('--adif-summary', dest='adif_from_summary', action='store_true')
    parser.add_argument('--adif', metavar='ADIF', nargs='*')
    parser.add_argument('--debug', dest='debug', action='store_true')
    parser.add_argument('--valid-only', dest='valid_only', action='store_true')
    parser.add_argument('--score-only', dest='score_only', action='store_true')
    parser.set_defaults(debug=False)
    parser.set_defaults(adif_from_summary=False)
    parser.set_defaults(valid_only=False)
    parser.set_defaults(score_only=False)
    args = parser.parse_args()

    summary = contests.summary_parser(args.summary, args.delim)
    adif_files = {}
    if args.adif_from_summary:
        adif = summary[args.call.upper()]['adifFile']
        try:
            rootname, ext = os.path.splitext(adif)
        except FileNotFoundError:
            print('File {} not found; skipping'.format(adif), file=sys.stderr)
        else:
            name = os.path.basename(rootname)
            adif_files[name] = adifparser.parse(adif)
    else:
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

    conditions = {
        'valid_modes': ['psk', 'bpsk', 'psk31', 'bpsk31', 'qpsk31'],
        'valid_bands': ['10m', '15m', '20m', '40m', '80m'],
    }
    if args.year == '2021':
        conditions['contest_start'] = datetime.datetime(2021, 1, 2, 0, 0, 0, 0)
        conditions['contest_end'] = datetime.datetime(2021, 1, 2, 23, 59, 59, 0)
    elif args.year == '2020':
        conditions['contest_start'] = datetime.datetime(2020, 1, 4, 0, 0, 0, 0)
        conditions['contest_end'] = datetime.datetime(2020, 1, 4, 23, 59, 59, 0)
    elif args.year == '2019':
        conditions['contest_start'] = datetime.datetime(2019, 1, 5, 0, 0, 0, 0)
        conditions['contest_end'] = datetime.datetime(2019, 1, 5, 23, 59, 59, 0)
    else:
        print("No year given: Exiting", file=sys.stderr)
        exit(1)

    valid_entries, invalid_entries, scores = contests.pskfest(adif_files, conditions, summary[args.call.upper()])

    if args.debug:
        pprint.pprint(valid_entries)
        pprint.pprint(summary)
        pprint.pprint(scores)
        pprint.pprint(invalid_entries)

    if args.score_only:
        contests.print_score(scores, summary[args.call.upper()])
    else:
        contests.print_title_block(summary[args.call.upper()])
        contests.print_score(scores, None)
        if valid_entries:
            contests.print_entries(valid_entries, valid=True)
        if not args.valid_only:
            if invalid_entries:
                contests.print_entries(invalid_entries, valid=False)
