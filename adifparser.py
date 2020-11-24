#!/usr/local/bin/python3
#
# adifparser.py
#
# Create dict of record info from adif input

# TODO: return header information along with records

import re
import sys
import fileinput
import pprint
import endorsements


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
    # we will stuff our record fields dictionaries in here
    record_elements = []
    # get raw record strings as a list
    raw_records = re.split('<EOR>[^<]*',linebuf,flags=re.IGNORECASE)
    # potential partial record to process later as the buffer
    leftover = raw_records.pop()
    
    for rec in raw_records:
        #print(rec)
        #TODO: Need to refine this to take into account fields that contain our separator "<"
        #       for example, <comment:25><a comment with brackets>  breaks the split because
        #       it thinks <a comment with brackets> is a field
        elements = rec.split('<')
        # Clean up leading stuff (newlines before the record, etc)
        elements.pop(0)
        fields = {}
        fields['errors'] = [] # bucket for broken stuff
        for element in elements:
            field = element.split('>')
            field_info = field[0].split(':')
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
            # use the length to strip off extra characters in the data so only the 
            # actual data is stored
            try:
                # TODO: Add a check that length of the field data matches the value we've been given
                #       Part of the problem here is string length gets confused by newlines, so a
                #       simple comparison isn't accurate (ie, as-is, this will truncate)
                fields[field_name]['data'] = field[1][0:fields[field_name]['length']]
            except:
                fields['errors'].append(field_info)
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
    with fileinput.input(inputfile,openhook=fileinput.hook_encoded("ISO-8859-1") ) as f:
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
    import argparse

    parser = argparse.ArgumentParser(description='ADIF Parser')
    parser.add_argument('inputfile', metavar='ADIF')
    args = parser.parse_args()

    records = parse(args.inputfile)

    for rec in records:
        try:
            print("<CALL:{}>{} <BAND:{}>{} <QSO_DATE:{}>{} <TIME_ON:{}>{} <MODE:{}>{}".format(  
                rec['call']['length'], 
                rec['call']['data'],
                rec['band']['length'],
                rec['band']['data'],
                rec['qso_date']['length'],
                rec['qso_date']['data'],
                rec['time_on']['length'],
                rec['time_on']['data'],
                rec['mode']['length'],
                rec['mode']['data'],
                )
            )
        except KeyError:
            print("KeyError for record",file=sys.stderr)
        for key in sorted(rec):
            print("<{}:{}>{} ".format(key,rec[key]['length'],rec[key]['data']))
