#!/usr/local/bin/python3
#
# contests.py
#
# module for calculating contest results


def triple_play_2019(adif, summary):
    results = {} # going to stuff scorer results for all the entries here
    valid_modes = ['psk', 'bpsk', 'psk31', 'bpsk31', 'qpsk31']
    valid_dates = [20191109, 20191110, 20191111]
    categories = {5 : 'QRP 5 watts',
                  25 : 'Low Power 25 watts',
                  50 : 'Medium Power 50 watts',
                  100 : 'High Power 100 watts',
                  }
    # loop through adif files
    # for each adif file, grab summary info
    for entry in adif:
        print(entry,len(adif[entry]))
        print(summary[entry])


def summary_parser(inputfile):
    import csv
    summary = {}
    with open(inputfile, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            summary[row['callsign']] = row
    return summary


if __name__ == '__main__':
    import adifparser
    import argparse
    import pprint

    parser = argparse.ArgumentParser(description='Contests Checker')
    parser.add_argument('--summary', metavar='SUMMARY')
    parser.add_argument('--adif', metavar='ADIF', nargs='*')
    args = parser.parse_args()

    summary = summary_parser(args.summary)
    adif_records = {}
    for adif in args.adif:
        name, ext = adif.split('.')
        adif_records[name] = adifparser.parse(adif)
    pprint.pprint(adif_records)
    pprint.pprint(summary)
    triple_play_2019(adif_records,summary)
