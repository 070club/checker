#!/usr/local/bin/python3
#
# vdsprint.py
#
# module for calculating Valentine's Day Sprint results

import sys
import adifparser
import contests
import argparse
import pprint
import os.path

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
    parser.set_defaults(adif_from_summary=False)
    parser.set_defaults(valid_only=False)
    parser.set_defaults(score_only=False)
    args = parser.parse_args()

    if args.year:
        # TODO: Move try block into set_conditions. This is too broad as-is
        try:
            conditions = contests.set_conditions(int(args.year), 'vdsprint')
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
    valid_entries, invalid_entries, scores = contests.vdsprint(adif_files, conditions, summary[args.call.upper()])

    if args.debug:
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
