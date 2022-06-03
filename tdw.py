#!/usr/local/bin/python3
#
# tdw.py
#
# module for calculating Three Day Weekend results

import sys

# TODO : Programmatically determine max member number from google sheet


def set_member_conditions(year, conditions):
    if year == 2022:
        conditions['bonus_stations'] = ['K3JT', 'KC3FL', 'KC4TIE', 'N6MG', 'NY7H', 'TI2YO', 'VA3TPS', 'WA5AMM']
        conditions['max_member'] = 2924  # TDW 2022 maximum
    elif year == 2021:
        conditions['bonus_stations'] = ['N5SLY', 'N9AVY', 'KB3RAN', 'N6MG', 'KC3FL', 'KE5PYF', 'KD6TR', 'VA7GEM']
        conditions['max_member'] = 2842  # TDW 2021 maximum
    elif year == 2020:
        conditions['bonus_stations'] = ['N5SLY', 'VA3TPS', 'KC3FL', 'N9AVY', 'KK6KMU', 'VA7GEM']
        conditions['max_member'] = 2759  # TDW 2020 maximum
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
        conditions = contests.set_conditions(int(args.year), 'tdw')
        conditions = set_member_conditions(int(args.year), conditions)
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

    valid_entries, invalid_entries, scores = contests.tdw(adif_files, conditions, summary[args.call.upper()])

    if args.debug:
        pprint.pprint(valid_entries)
        pprint.pprint(summary[args.call.upper()])
        pprint.pprint(scores)
        pprint.pprint(invalid_entries)

    if args.score_only:
        contests.print_score_tdw(scores, summary[args.call.upper()])
    else:
        contests.print_title_block_tdw(summary[args.call.upper()])
        contests.print_score_tdw(scores, None)
        if valid_entries:
            contests.print_entries_tdw(valid_entries, conditions['bonus_stations'], valid=True)
        if not args.valid_only:
            if invalid_entries:
                contests.print_entries_tdw(invalid_entries, conditions['bonus_stations'], valid=False)
