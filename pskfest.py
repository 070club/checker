#!/usr/local/bin/python3
#
# pskfest.py
#
# module for calculating pskfest results

def print_entries(entries,valid=True):
    if valid:
        print('\nValid QSOs')
        print_header(valid=True)
        for rec in entries:
            try:
                call = rec['call']['data'].upper()
            except:
                call = ''
            try:
                qso_date = rec['qso_date']['data']
            except:
                qso_date = ''
            try:
                time_on = rec['time_on']['data']
            except:
                time_on = ''
            try:
                band = rec['band']['data']
            except:
                band = ''
            try:
                srx_string = rec['srx_string']['data']
            except:
                srx_string = ''
            try:
                dxcc = rec['dxcc']['data']
            except:
                dxcc = ''
            try:
                state = rec['state']['data'].upper()
            except:
                state = ''
            try:
                print("{},{},{},{},{},{},{}".format(
                    call,
                    qso_date,
                    time_on,
                    band,
                    srx_string,
                    dxcc,
                    state,
                    )
                )
            except KeyError:
                print("KeyError for record", file=sys.stderr)
    else:
        print('\nBroken QSOs (check listed errors)')
        print_header(valid=False)
        for rec in entries:
            try:
                call = rec['data']['call']['data']
            except:
                call = ''
            try:
                qso_date = rec['data']['qso_date']['data']
            except:
                qso_date = ''
            try:
                time_on = rec['data']['time_on']['data']
            except:
                time_on = ''
            try:
                band = rec['data']['band']['data']
            except:
                band = ''
            try:
                srx_string = rec['data']['srx_string']['data']
            except:
                srx_string = ''
            try:
                dxcc = rec['data']['dxcc']['data']
            except:
                dxcc = ''
            try:
                state = rec['data']['state']['data']
            except:
                state = ''

            try:
                print("{},{},{},{},{},{},{},{}".format(
                    call,
                    qso_date,
                    time_on,
                    band,
                    srx_string,
                    dxcc,
                    state,
                    '|'.join(rec['errors']),
                    )
                )
            except KeyError:
                print("KeyError for record", file=sys.stderr)


def print_score(scores,summary):
    if summary: #Report only, spit out CSV of call+score
        callsign = summary['callsign']
        try:
            category = contests.categories[int(summary['category'])]
        except:
            category = 'unknown'
        try:
            podxs_number = summary['070-number']
        except:
            podxs_number = 'unknown'
        email = summary['email']
        q_points = scores['q-points']
        dxcc = len(scores['mults']['dxcc']['data'])
        state = len(scores['mults']['state'])
        total = scores['total']

        print('callsign,category,070-number,email,q-points,dxcc-mult,state-mult,total')
        print('{},{},{},{},{},{},{},{}'.format(
            callsign,
            category,
            podxs_number,
            email,
            q_points,
            dxcc,
            state,
            total,
            )
        )
    else:
        print('\nQs:{} DXCC:{} STATE:{} Total:{}'.format(
            scores['q-points'],
            len(scores['mults']['dxcc']['data']),
            len(scores['mults']['state']),
            scores['total']
            )
        )
        if scores['mults']['dxcc']['errors']:
            for error in scores['mults']['dxcc']['errors']:
                print('DXCC ERRORS: {},{},{}'.format(
                    error['call']['data'],
                    error['qso_date']['data'],
                    error['time_on']['data'],
                    )
                )


def print_header(valid=True):
    if valid:
        print("\ncall,qso_date,time_on,band,srx_string,dxcc,state")
    else:
        print("\ncall,qso_date,time_on,band,srx_string,dxcc,state,errors")


def print_title_block(summary):
    try:
        category = contests.categories[int(summary['category'])]
    except:
        category = 'unknown'
    try:
        podxs_number = summary['070-number']
    except:
        podxs_number = 'unknown'

    print('\nCALL:{}\nPOWER:{}\nEMAIL:{}\n'.format(
        summary['callsign'],
        category,
        summary['email'],
        )
    )


if __name__ == '__main__':
    import adifparser
    import contests
    import argparse
    import pprint

    parser = argparse.ArgumentParser(description='Contests Checker')
    parser.add_argument('--year', metavar='YEAR')
    parser.add_argument('--summary', metavar='SUMMARY')
    parser.add_argument('--call', metavar='CALL')
    parser.add_argument('--adif', metavar='ADIF', nargs='*')
    parser.add_argument('--debug', dest='debug', action='store_true')
    parser.add_argument('--valid-only', dest='valid_only', action='store_true')
    parser.add_argument('--score-only', dest='score_only', action='store_true')
    parser.set_defaults(debug=False)
    parser.set_defaults(valid_only=False)
    parser.set_defaults(score_only=False)
    args = parser.parse_args()

    summary = contests.summary_parser(args.summary)
    adif_files = {}
    for adif in args.adif:
        name, ext = adif.split('.')
        adif_files[name] = adifparser.parse(adif)

    if args.year == '2019':
        valid_entries, invalid_entries, scores = contests.pskfest_2019(adif_files,summary)
    if args.year == '2020':
        valid_entries, invalid_entries, scores = contests.pskfest_2020(adif_files,summary)

    if args.debug:
        pprint.pprint(valid_entries)
        pprint.pprint(summary)
        pprint.pprint(invalid_entries)

    if args.score_only:
        print_score(scores,summary[args.call.upper()])
    else:
        print_title_block(summary[args.call.upper()])
        print_score(scores,None)
        if valid_entries:
            print_entries(valid_entries,valid=True)
        if not args.valid_only:
            if invalid_entries:
                print_entries(invalid_entries,valid=False)

