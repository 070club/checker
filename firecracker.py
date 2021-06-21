#!/usr/local/bin/python3
#
# firecracker.py
#
# module for calculating the Firecracker Sprint results

import sys
import datetime
import calendar


def get_contest_day(year, month):
    """ Find the first Saturday of the month after July 1st and return it """
    # TODO: Rework with standard Monday as first day so calendar.SATURDAY works
    calendar.setfirstweekday(6) # Set start of week to Sunday
    cal = calendar.monthcalendar(year, month)
    if args.debug:
        print("first weekday: {}".format(calendar.firstweekday()))
        pprint.pprint(cal)
    first_week = cal[0]
    second_week = cal[1]
    if first_week[-1] == 1: # [-1] is Saturday
        if args.debug:
            pprint.pprint(second_week)
        return second_week[-1]
    else:
        if args.debug:
            pprint.pprint(first_week)
        return first_week[-1]


def set_conditions(year):
    contest_day = get_contest_day(year, 7)
    conditions = {
        'valid_modes': ['psk', 'bpsk', 'psk31', 'bpsk31', 'qpsk31', ],
        'valid_bands': ['40m'],
        'contest_start': datetime.datetime(year, 7, contest_day, 20, 00, 00, 0),
        'contest_end': datetime.datetime(year, 7, contest_day+1, 19, 59, 59, 0),
    }
    return conditions


if __name__ == '__main__':
    import adifparser
    import contests
    import argparse
    import pprint
    import os.path

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

    if args.year:
        # TODO: Move try block into set_conditions. This is too broad as-is
        try:
            conditions = set_conditions(int(args.year))
        except ValueError:
            print("Invalid year given (must be in the form YYYY): Exiting", file=sys.stderr)
            exit(1)
    else:
        print("No year given: Exiting", file=sys.stderr)
        exit(1)

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

    valid_entries = None
    invalid_entries = None
    scores = None

    valid_entries, invalid_entries, scores = contests.firecracker(adif_files, conditions, summary[args.call.upper()])

    if args.debug:
        pprint.pprint(valid_entries)
        pprint.pprint(summary[args.call.upper()])
        pprint.pprint(scores)
        pprint.pprint(invalid_entries)

    if args.score_only:
        contests.print_score(scores, summary[args.call.upper()])
    else:
        contests.print_title_block_startblock(summary[args.call.upper()])
        contests.print_score(scores, None)
        if valid_entries:
            contests.print_entries(valid_entries, valid=True)
        if not args.valid_only:
            if invalid_entries:
                contests.print_entries(invalid_entries, valid=False)
