#!/usr/local/bin/python3
#
# adifparser.py
#
# Create dict of record info from adif input

# TODO: return header information along with records
# TODO: return error if not an ADIF file
# TODO: write a cabrillo parser
# TODO: write a log parser manager (higher-level call that picks which type to use; ADIF, cabrillo, etc)
# TODO: Throw out invalid records (ie, test for invalid call, date/time, etc)

import re
import sys
import fileinput
#import magic # using python-magic


def parse_header(linebuf):
    # we will stuff our record fields dictionaries in here
    header_elements = []
    # get raw record strings as a list
    raw_header = re.split('<EOH>[^<]*',linebuf,flags=re.IGNORECASE)
    # potential partial record to process later as the buffer
    leftover = raw_header.pop()
    
    for rec in raw_header:
        elements = rec.split('<')
        fields = {}
        fields['freeform'] = []
        for element in elements:
            field = element.split('>')
            field_info = field[0].split(':')
            fields[field_info[0]] = {}
            try:
                fields[field_info[0]]['length'] = int(field_info[1])
                # use the length to strip off extra characters in the data
                fields[field_info[0]]['data'] = field[1][0:int(field_info[1])]
            except:
                fields['freeform'].append(field)

        header_elements.append(fields)
    return header_elements,leftover


def parse_record(linebuf):

    # regex for splitting ADIF elements
    element_re = re.compile('(<[^>]*:+\d+:*[BNDTSIMGELbndtsimgel]?>)')
    # we will stuff our record fields dictionaries in here
    record_elements = []
    # get raw record strings as a list
    raw_records = re.split('<EOR>[^<]*',linebuf,flags=re.IGNORECASE)
    # potential partial record to process later as the buffer
    leftover = raw_records.pop()
    
    for rec in raw_records:
        elements = re.split(element_re, rec)
        # Clean up leading stuff (newlines before the record, etc)
        elements.pop(0)
        fields = {}
        fields['errors'] = [] # bucket for broken stuff
        field_name = False
        for element in elements:
            if field_name:
                stripped_element = element.strip()
                try:
                    fields[field_name]['data'] = stripped_element[:fields[field_name]['length']]
                    if fields[field_name]['length'] != len(fields[field_name]['data']):
                        fields[field_name]['length'] = len(fields[field_name]['data'])
                except:
                    fields['errors'].append(field_name)
                field_name = False
            else:
                field = element.strip('<>')
                field_info = field.split(':')
                if len(field_info) < 2:
                    # something is wrong here.  We don't have the right number of items
                    fields['errors'].append(element)
                    continue
                field_name = field_info[0].lower()
                fields[field_name] = {}
                try:
                    fields[field_name]['length'] = int(field_info[1])
                except:
                    fields['errors'].append(field_info)
                try:
                    fields[field_name]['type'] = field_info[2]
                except:
                    pass
        if len(fields['errors']) == 0:
            del(fields['errors'])
#        if fields['mode']['data'].lower() in ['psk','bpsk','psk31','bpsk31','qpsk31']: # We want only PSK31 QSOs
#            record_elements.append(fields)
        # There's no point appending if the record is empty (ie, the ADIF is empty)
        if len(fields) > 0:
            record_elements.append(fields)
    return record_elements,leftover


def parse(inputfile):
    ''' ADIF file parser
        takes input file and returns a list of dict records
    '''

    header = None
    records = []
    linebuf = ''

    #TODO: add field validation (eg, make sure state info is valid - "ON // ONTARIO" ?)

    # need to determine what kind of encoding to do on the input file, or just try a couple
    # different common encodings (latin1, utf-8, etc).  utf-8 likes the slash zero, but not
    # accented letters
    #detected = magic.detect_from_filename(inputfile)
    encoding = 'ISO-8859-1'

    with fileinput.input(inputfile, openhook=fileinput.hook_encoded(encoding)) as f:
        for line in f:
            if fileinput.isfirstline():
                if line[0] == '<':
                    in_header = False
                else:
                    in_header = True
            linebuf = linebuf + line
            if in_header:
                if '<eoh>' in line.lower():
                    header,linebuf = parse_header(linebuf)
                    in_header = False
            else:
                if '<eor>' in line.lower():
                    record,linebuf = parse_record(linebuf)
                    for rec in record:
                        records.append(rec)

    return records


if __name__ == '__main__':
    import csv
    import argparse

    parser = argparse.ArgumentParser(description='ADIF Parser')
    parser.add_argument('-i', '--inputfile', action='store', dest='inputfile', metavar='ADIF', required=True)
    parser.add_argument('-o', '--format', dest='format', default='csv', help='Output format: csv(default), txt')
    parser.add_argument('-f', '--fields', dest='fields', nargs='*', help='List of output fields',
                                            default=['call','qso_date','time_on','band','mode'])
    parser.add_argument('-d', '--debug', dest='debug', help='Debug flag', action='store_true')
    parser.set_defaults(debug=False)
    args = parser.parse_args()
    if args.debug:
        print(args)

    records = parse(args.inputfile)
    headers = args.fields

    if args.format == 'text':
        output_writer = csv.writer(sys.stdout, delimiter=' ', quoting=csv.QUOTE_ALL)
    elif args.format == 'csv':
        output_writer = csv.writer(sys.stdout, dialect='excel', quoting=csv.QUOTE_ALL)
    output_writer.writerow(headers)

    for rec in records:
        output_record = []
        for header in headers:
            try:
                output_record.append(rec[header]['data'])
            except KeyError:
                output_record.append('data not found')
        output_writer.writerow(output_record)

    if args.debug:
        for rec in records:
            print("\n--- NEW RECORD ---")
            for key in sorted(rec):
                print("<{}:{}>{} ".format(key, rec[key]['length'], rec[key]['data']))
