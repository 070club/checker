#!/usr/local/bin/python3
#
# thirtyone.py
#
# module for calculating 31 Flavors results

import sys
import adifparser
import calendar
import datetime
import contests
import argparse
import pprint
import os.path


def get_contest_day(year, month):
    """ Find the first Saturday of the month and return it """
    cal = calendar.monthcalendar(int(year), month)
    if args.debug:
        pprint.pprint(cal)
    first_week = cal[0]
    second_week = cal[1]
    if first_week[calendar.SATURDAY]:
        return first_week[calendar.SATURDAY]
    else:
        return second_week[calendar.SATURDAY]


def set_conditions(year):
    conditions = {
        'valid_modes': ['psk', 'bpsk',
                        'psk31', 'bpsk31', 'qpsk31',
                        'psk63', 'bpsk63', 'qpsk63',
                        'psk125', 'bpsk125', 'qpsk125',
                        ],
        'valid_bands': ['20m'],
    }
    contest_day = get_contest_day(year, 4)
    conditions['contest_start'] = datetime.datetime(year, 4, contest_day, 10, 0, 0, 0)
    conditions['contest_end'] = datetime.datetime(year, 4, contest_day+1, 3, 59, 59, 0)
    return conditions


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='31 Flavors Contests Checker')
    parser.add_argument('--year', metavar='YEAR')
    parser.add_argument('--summary', metavar='SUMMARY')
    parser.add_argument('--delim', metavar='DELIMITER', default=',' )
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
        adif = summary[args.call.upper()]['adif_file']
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

    if args.year:
        conditions = set_conditions(int(args.year))
    else:
        print("No year given: Exiting", file=sys.stderr)
        exit(1)

    valid_entries, invalid_entries, scores = contests.thirtyone_flavors(adif_files, conditions, summary[args.call.upper()])

    if args.debug:
        pprint.pprint(valid_entries)
        pprint.pprint(summary[args.call.upper()])
        pprint.pprint(scores)
        pprint.pprint(invalid_entries)

    if args.score_only:
        contests.print_score_31flavors(scores, summary[args.call.upper()])
    else:
        contests.print_title_block_startblock(summary[args.call.upper()])
        contests.print_score_31flavors(scores, None)
        if valid_entries:
            contests.print_entries_31flavors(valid_entries, valid=True)
        if not args.valid_only:
            if invalid_entries:
                contests.print_entries_31flavors(invalid_entries, valid=False)
