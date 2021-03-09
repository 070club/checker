#!/usr/local/bin/python3
#
# saintpat.py
#
# module for calculating St. Patrick's Day results

import adifparser
import contests
import calendar
import datetime
import argparse
import pprint
import os.path
import sys


def get_contest_day(year, month):
    """ Find the third Saturday of the month and return it """
    cal = calendar.monthcalendar(int(year), month)
    if args.debug:
        pprint.pprint(cal)
    first_week = cal[0]
    third_week = cal[2]
    fourth_week = cal[3]
    if first_week[calendar.SATURDAY]:
        return third_week[calendar.SATURDAY]
    else:
        return fourth_week[calendar.SATURDAY]

def set_conditions(year):
    conditions = {
        'valid_modes': ['psk', 'bpsk', 'psk31', 'bpsk31', 'qpsk31'],
        'valid_bands': ['6m', '10m', '15m', '20m', '40m', '80m', '160m'],
    }
    contest_day = get_contest_day(year, 3)
    conditions['contest_start'] = datetime.datetime(year, 3, contest_day, 0, 0, 0, 0)
    conditions['contest_end'] = datetime.datetime(year, 3, contest_day, 23, 59, 59, 0)
    return conditions


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Contests Checker')
    parser.add_argument('--year', metavar='YEAR')
    parser.add_argument('--summary', metavar='SUMMARY')
    parser.add_argument('--delim', metavar='DELIMITER', default=',' )
    parser.add_argument('--call', metavar='CALL')
    parser.add_argument('--adif', metavar='ADIF', nargs='*')
    parser.add_argument('--adif-summary', dest='adif_from_summary', action='store_true')
    parser.add_argument('--debug', dest='debug', action='store_true')
    parser.add_argument('--valid-only', dest='valid_only', action='store_true')
    parser.add_argument('--score-only', dest='score_only', action='store_true')
    parser.set_defaults(debug=False)
    parser.set_defaults(valid_only=False)
    parser.set_defaults(score_only=False)
    parser.set_defaults(adif_from_summary=False)
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

    if args.year:
        conditions = set_conditions(int(args.year))
    else:
        print("No year given: Exiting", file=sys.stderr)
        exit(1)

    valid_entries, invalid_entries, scores = contests.saintpats(adif_files, conditions, summary[args.call.upper()])

    if args.debug:
        pprint.pprint(conditions)
        pprint.pprint(valid_entries)
        pprint.pprint(summary[args.call.upper()])
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
