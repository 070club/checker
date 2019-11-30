#!/usr/local/bin/python3
#
# endorsements.py
#
# module for keeping track of endorsement details
# eventually, this is where methods for checking 
# each endorsement will live

# US prefix information https://www.fcc.gov/amateur-call-sign-systems

import sys
import re

#####
#####
#####  REMEMBER TO CHECK FOR DATES ON DATE-SPECIFIC ENDORSEMENTS
#####
#####

##### global re match objects #####
#Hawaii
hawaii_prefix = re.compile('^[AKNW]H[67][^/][^/]*$', flags=re.IGNORECASE)
hawaii_suffix = re.compile('^[^/][^/]*/[AKNW]H[67]$', flags=re.IGNORECASE)

#Endorsements with contacts from the Pacific and Down Under

# Aloha
# If you've worked Hawaii on PSK31, you qualify for the "Aloha" endorsement.

def aloha(records):
    '''take list of records and see if requirements are met.
    return record details of first entry that matches requirement'''

    for rec in records:
        try:
            if rec['dxcc']['data'] == '110':
                return rec
        except:
            print("no DXCC",rec['call']['data'], rec['qso_date']['data'],file=sys.stderr)
    return None

 
# China Clipper
# Fly the 070 Club's version of the China Clipper route and earn this "China
# Clipper" endorsement. To qualify work California, Hawaii, Japan, Taiwan and the
# Philippines on PSK31. Valid contacts are those made after 4 July 2001.

def china_clipper(records):
    '''take list of records and see if requirements are met.
    return dict of records that match, and a dict of what's missing'''

    found = { 'Taiwan': None,
                'Philippines': None,
                'Hawaii': None,
                'California': None,
                'Japan': None,
                }

    missing = { 'Taiwan':'BV', 
                'Philippines':'DU',
                'Hawaii':'KH6',
                'California':'K,CA',
                'Japan':'JA',
                }

    for rec in records:
        if int(rec['qso_date']['data']) > 20010704:
            if 'Hawaii' in missing:
                try:
                    if rec['dxcc']['data'] == '110':
                        found['Hawaii'] = rec
                        missing.pop('Hawaii',None)
                        continue
                except:
                    print("no DXCC",rec['call']['data'], rec['qso_date']['data'],file=sys.stderr)
            if 'Taiwan' in missing:
                try:
                    if rec['dxcc']['data'] == '386':
                        found['Taiwan'] = rec
                        missing.pop('Taiwan',None)
                        continue
                except:
                    print("no DXCC",rec['call']['data'], rec['qso_date']['data'],file=sys.stderr)
            if 'Philippines' in missing:
                try:
                    if rec['dxcc']['data'] == '375':
                        found['Philippines'] = rec
                        missing.pop('Philippines',None)
                        continue
                except:
                    print("no DXCC",rec['call']['data'], rec['qso_date']['data'],file=sys.stderr)
            if 'California' in missing:
                try:
                    if (rec['dxcc']['data'] == '291' and rec['state']['data'].lower() == 'ca'):
                        found['California'] = rec
                        missing.pop('California',None)
                        continue
                except:
                    print("no DXCC",rec['call']['data'], rec['qso_date']['data'],file=sys.stderr)
            if 'Japan' in missing:
                try:
                    if rec['dxcc']['data'] == '339':
                        found['Japan'] = rec
                        missing.pop('Japan',None)
                        continue
                except:
                    print("no DXCC",rec['call']['data'], rec['qso_date']['data'],file=sys.stderr)

    return found,missing
 
# Wrk'd All Oz
# If you have all six Australian states and the two territories in the log on
# PSK31, then you've earned yourself the "Wrk'd All Oz" endorsement, mate! Valid
# contacts are those made with Western Australia, South Australia, Queensland,
# New South Wales, Victoria, Tasmania, Northern Territory, and Australian Capital
# Territory.
 
 
# Endorsements with Special Stations
# 
# 88 Tri-Band
# Work three different female 070 Club members on PSK31 (one each on any three
# different HF bands, 160M thru 6M) and earn this "88 Tri-Band" endorsement.
# Valid contacts are those made on or after 1 July 2002.
# 
# K3VOA
# Thanks to the efforts of K3NJ, the Voice of America ARC (QTH Washington, DC)
# is now a bona fide member of the 070 Club. If you worked K3VOA on or after 8
# August 2001, you qualify for the " K3VOA" endorsement.
# 
# QRP
# Hey QRPers, get a QRP-sized bumper sticker for your 070 certificate! Brag
# file only required listing your QRP set-up (max output 5 watts).
# 
# QRP Tri-Band
# Work three different stations using PSK31/QRP. Contacts must be two way QRP
# (5W or less) and may be made on any three different HF bands of your choice
# (160M-6M). Valid contacts are those made after 31 December 2002.
 
 
# WABOL
# 
# WABOL 2019
# Work 50 2x LONP (both 070 members are also LONP at time of QSO) during the calendar year.
# Expires 2019-12-31
# 
# Where in the world is Steve?
# Work Steve W3HF while he's in 4 different places. This is an unofficial
# award, and is run by Steve W3HF who provides a custom certificate.

 
# Endorsements for contacts with North and South America
# 
# Nunavut and the Rest of It - NA above 60
# Work FOUR of these five entities - Nunavut, Northwest Territory, Yukon
# Territory, Alaska and Greenland starting 2014-09-01.
# 
# Alaska
# If you have Alaska in the log on PSK31, you qualify for the "Alaska"
# endorsement.
# 
# Central-America
# Work all seven countries of Central America on PSK31 and add the Central
# America endorsement to your certificate: (Belize, Costa Rica, El Salvador,
# Guatemala, Honduras, Nicaragua and Panama).
# 
# Lower 48
# If you've worked the entire continental United States (lower 48 states) on
# PSK31, you qualify for the "Lower 48" endorsement. Valid contacts are those
# made after 1 June 2000.
# 
# Maple Leaf
# To earn the "Maple Leaf" endorsement, put the ten Canadian provinces in the
# log on PSK31: Alberta, British Columbia, Manitoba, New Brunswick,
# Newfoundland, Nova Scotia, Ontario, Prince Edward Island, Quebec, and
# Saskatchewan.
# 
# South American PSK31
# 
# South American PSK31 [4]
# Announcing the South American PSK31 endorsement series! These endorsements
# shall be issued in a series of 3 separate endorsements. To earn the South
# American PSK31 endorsements, work the required number of political entities
# (4, 7, or the maximum 13) which make up the South American continent (see
# list below) using PSK31 mode on the hf bands. Valid contacts are those made
# after 27 May 2010 UTC. All stations worked must be located on continental
# South America, off-shore dependencies not valid (eg Easter Is). The following
# 13 South American political entities are valid for this endorsement:
# Argentina, Bolivia, Brazil, Chile, Colombia, Ecuador, Fr. Guiana, Guyana,
# Paraguay, Peru, Suriname, Uruguay, Venezuela.
# 
# South American PSK31 [7]
# Work seven total South American political entities.
# 
# South American PSK31 [13]
# Work thirteen total South American political entities.
 
 
# TripleDouble
# 
# DakotaDouble
# Work 1 ND and 1 SD station starting 2014-09-01.
# 
# VirginiaDouble
# Work 1 VA and 1 WV station starting 2014-09-01.
# 
# CarolinaDouble
# Work 1 NC and 1 SC station starting 2014-09-01.
# 
# TripleDouble
# Work 10 station-bands in the Dakotas (ND/SD), 10 station-bands in the
# Virginias (VA/WV), and 10 station-bands in the Carolinas (NC/SC).
# DakotaDouble, VirginiaDouble, and CarolinaDouble are pre-requisites (same
# QSOs may be used for TripleDouble). QSOs starting 2014-09-01.
# 
# 
# US-CONUS-GRIDS
# 
# CONUS Grids [50]
# Work US stations in 436 of the 488 CONUS gridsquares, in increments of 50. We
# took the ARRL FFMA map
# (http://www.arrl.org/files/file/FFMA/FFMA_2010Map-C.pdf) and excluded the
# following (nearly all water or VE/XE): CM79 CM86 CM93 CM94 CN70 CN72 CN73
# CN74 CN75 CN76 CN77 CN78 DL79 DL98 DM02 DM03 DM12 DM22 DM31 DM61 EL15 EL28
# EL58 EL79 EL84 EL86 EN29 EN48 EN57 EN58 EN62 EN63 EN64 EN67 EN85 EN86 EN92
# FM02 FM13 FM25 FM26 FM27 FN03 FN14 FN25 FN35 FN46 FN51 FN53 FN57 FN66 FN67
# 
# CONUS Grids [100]
# Work US stations in 436 of the 488 CONUS gridsquares, in increments of 50.
# 
# CONUS Grids [150]
# Work US stations in 436 of the 488 CONUS gridsquares, in increments of 50.
# 
# CONUS Grids [200]
# Work US stations in 436 of the 488 CONUS gridsquares, in increments of 50.
# 
# CONUS Grids [250]
# Work US stations in 436 of the 488 CONUS gridsquares, in increments of 50.
# 
# CONUS Grids [300]
# Work US stations in 436 of the 488 CONUS gridsquares, in increments of 50.
# 
# CONUS Grids [350]
# Work US stations in 436 of the 488 CONUS gridsquares, in increments of 50.
# 
# CONUS Grids [400]
# Work US stations in 436 of the 488 CONUS gridsquares, in increments of 50.
# 
# CONUS Grids [ALL]
# Work US stations in 436 of the 488 CONUS gridsquares, in increments of 50.
# 
# 
# US-STATE-GRIDS
# 
# AL State Grids
# Work this state's primary grids (w/any US station in the grid): EM50 EM51
# EM52 EM53 EM54 EM60 EM61 EM62 EM63 EM64 EM71 EM72 EM73 EM74
# 
# AR State Grids
# Work this state's primary grids (w/any US station in the grid): EM23 EM24
# EM25 EM26 EM33 EM34 EM35 EM36 EM43 EM44 EM45 EM46 EM55
# 
# AZ State Grids
# Work this state's primary grids (w/any US station in the grid): DM23 DM24
# DM25 DM26 DM32 DM33 DM34 DM35 DM36 DM41 DM42 DM43 DM44 DM45 DM46 DM51 DM52
# DM53 DM54 DM55 DM56
# 
# CA State Grids
# Work this state's primary grids (w/any US station in the grid): CM87 CM88
# CM89 CM95 CM96 CM97 CM98 CM99 CN71 CN80 CN81 CN90 CN91 DM04 DM05 DM06 DM07
# DM08 DM13 DM14 DM15 DM16 DM17 DM23 DM24 DM25 DM26
# 
# CO State Grids
# Work this state's primary grids (w/any US station in the grid): DM57 DM58
# DM59 DM67 DM68 DM69 DM77 DM78 DM79 DM87 DM88 DM89 DN50 DN60 DN70 DN80
# 
# 
# CT State Grids
# Work this state's primary grids (w/any US station in the grid): FN31 FN32
# FN41 FN42
# 
# 
# DE State Grids
# Work this state's primary grids (w/any US station in the grid): FM28 FM29
# 
# 
# FL State Grids
# Work this state's primary grids (w/any US station in the grid): EL87 EL88
# EL89 EL94 EL95 EL96 EL97 EL98 EL99 EM60 EM70 EM80 EM90
# 
# 
# GA State Grids
# Work this state's primary grids (w/any US station in the grid): EM70 EM71
# EM72 EM73 EM74 EM80 EM81 EM82 EM83 EM84 EM90 EM91 EM92 EM93
# 
# 
# IA State Grids
# Work this state's primary grids (w/any US station in the grid): EN11 EN12
# EN13 EN20 EN21 EN22 EN23 EN30 EN31 EN32 EN33 EN40 EN41 EN42 EN43
# 
# 
# ID State Grids
# Work this state's primary grids (w/any US station in the grid): DN12 DN13
# DN14 DN15 DN16 DN17 DN18 DN22 DN23 DN24 DN25 DN26 DN27 DN32 DN33 DN34 DN35
# DN42 DN43 DN44
# 
# 
# IL State Grids
# Work this state's primary grids (w/any US station in the grid): EM48 EM49
# EM57 EM58 EM59 EM68 EM69 EN40 EN41 EN42 EN50 EN51 EN52 EN60 EN61
# 
# 
# IN State Grids
# Work this state's primary grids (w/any US station in the grid): EM67 EM68
# EM69 EM78 EM79 EN60 EN61 EN70 EN71 EM57
# 
# 
# KS State Grids
# Work this state's primary grids (w/any US station in the grid): DM97 DM98
# DM99 EM07 EM08 EM09 EM17 EM18 EM19 EM27 EM28 EM29
# 
# 
# KY State Grids
# Work this state's primary grids (w/any US station in the grid): EM56 EM57
# EM66 EM67 EM76 EM77 EM78 EM79 EM86 EM87 EM88
# 
# 
# LA State Grids
# Work this state's primary grids (w/any US station in the grid): EL39 EL49
# EL59 EM30 EM31 EM32 EM40 EM41 EM42 EM50
# 
# 
# MA State Grids
# Work this state's primary grids (w/any US station in the grid): FN32 FN41
# FN42
# 
# 
# MD State Grids
# Work this state's primary grids (w/any US station in the grid): FM09 FM18
# FM19 FM28 FM29
# 
# 
# ME State Grids
# Work this state's primary grids (w/any US station in the grid): FN43 FN44
# FN45 FN54 FN55 FN56 FN64 FN65
# 
# 
# MI State Grids
# Work this state's primary grids (w/any US station in the grid): EN46 EN55
# EN56 EN61 EN65 EN66 EN71 EN72 EN73 EN74 EN75 EN76 EN81 EN82 EN83 EN84
# 
# 
# MN State Grids
# Work this state's primary grids (w/any US station in the grid): EN13 EN14
# EN15 EN16 EN17 EN18 EN23 EN24 EN25 EN26 EN27 EN28 EN33 EN34 EN35 EN36 EN37
# EN38 EN43 EN44 EN46 EN47
# 
# 
# MO State Grids
# Work this state's primary grids (w/any US station in the grid): EM26 EM27
# EM28 EM29 EM36 EM37 EM38 EM39 EM46 EM47 EM48 EM49 EM56 EM57 EN20 EN30 EN40
# 
# 
# MS State Grids
# Work this state's primary grids (w/any US station in the grid): EM41 EM42
# EM43 EM44 EM50 EM51 EM52 EM53 EM54
# 
# 
# MT State Grids
# Work this state's primary grids (w/any US station in the grid): DN25 DN26
# DN27 DN28 DN34 DN35 DN36 DN37 DN38 DN44 DN45 DN46 DN47 DN48 DN55 DN56 DN57
# DN58 DN65 DN66 DN67 DN68 DN75 DN76 DN77 DN78
# 
# 
# NC State Grids
# Work this state's primary grids (w/any US station in the grid): EM75 EM85
# EM86 EM95 EM96 FM03 FM04 FM05 FM06 FM14 FM15 FM16
# 
# 
# ND State Grids
# Work this state's primary grids (w/any US station in the grid): DN86 DN87
# DN88 DN96 DN97 DN98 EN06 EN07 EN08 EN16 EN17 EN18
# 
# 
# NE State Grids
# Work this state's primary grids (w/any US station in the grid): DN81 DN82
# DN90 DN91 DN92 EN00 EN01 EN02 EN10 EN11 EN12 EN20 EN21
# 
# 
# NH State Grids
# Work this state's primary grids (w/any US station in the grid): FN32 FN33
# FN42 FN43 FN44 FN45
# 
# 
# NJ State Grids
# Work this state's primary grids (w/any US station in the grid): FM28 FM29
# FN20 FN21 FN30 FN31
# 
# 
# NM State Grids
# Work this state's primary grids (w/any US station in the grid): DM51 DM52
# DM53 DM54 DM55 DM56 DM62 DM63 DM64 DM65 DM66 DM72 DM73 DM74 DM75 DM76 DM82
# DM83 DM84 DM85 DM86
# 
# 
# NV State Grids
# Work this state's primary grids (w/any US station in the grid): DM07 DM08
# DM09 DM16 DM17 DM18 DM19 DM25 DM26 DM27 DM28 DM29 DN00 DN01 DN10 DN11 DN20
# DN21
# 
# 
# NY State Grids
# Work this state's primary grids (w/any US station in the grid): FN02 FN12
# FN13 FN20 FN21 FN22 FN23 FN24 FN30 FN31 FN32 FN33 FN34 FN41
# 
# 
# OH State Grids
# Work this state's primary grids (w/any US station in the grid): EM79 EM88
# EM89 EM99 EN70 EN71 EN80 EN81 EN90 EN91
# 
# 
# OK State Grids
# Work this state's primary grids (w/any US station in the grid): DM86 DM96
# EM04 EM05 EM06 EM13 EM14 EM15 EM16 EM23 EM24 EM25 EM26
# 
# 
# OR State Grids
# Work this state's primary grids (w/any US station in the grid): CN82 CN83
# CN84 CN85 CN92 CN93 CN94 CN95 DN02 DN03 DN04 DN05 DN12 DN13 DN14 DN15
# 
# 
# PA State Grids
# Work this state's primary grids (w/any US station in the grid): EM99 EN90
# EN91 FM09 FM19 FM29 FN00 FN01 FN10 FN11 FN20 FN21 FN02
# 
# 
# RI State Grids
# Work this state's primary grids (w/any US station in the grid): FN41 FN42
# 
# 
# SC State Grids
# Work this state's primary grids (w/any US station in the grid): EM83 EM84
# EM85 EM92 EM93 EM94 EM95 FM03 FM04
# 
# 
# SD State Grids
# Work this state's primary grids (w/any US station in the grid): DN83 DN84
# DN85 DN93 DN94 DN95 EN02 EN03 EN04 EN05 EN12 EN13 EN14 EN15
# 
# 
# TN State Grids
# Work this state's primary grids (w/any US station in the grid): EM45 EM55
# EM56 EM65 EM66 EM75 EM76 EM85 EM86 EM96
# 
# 
# TX State Grids
# Work this state's primary grids (w/any US station in the grid): DL88 DL89
# DL99 DM70 DM71 DM80 DM81 DM82 DM83 DM84 DM85 DM86 DM90 DM91 DM92 DM93 DM94
# DM95 DM96 EL06 EL07 EL08 EL09 EL16 EL17 EL18 EL19 EL29 EL39 EM00 EM01 EM02
# EM03 EM04 EM10 EM11 EM12 EM13 EM20 EM21 EM22 EM23 EM30 EM31
# 
# 
# UT State Grids
# Work this state's primary grids (w/any US station in the grid): DM37 DM38
# DM39 DM47 DM48 DM49 DM57 DM58 DM59 DN30 DN31 DN40 DN41 DN50
# 
# 
# VA State Grids
# Work this state's primary grids (w/any US station in the grid): EM86 EM87
# EM96 EM97 FM06 FM07 FM08 FM09 FM16 FM17 FM18 FM19
# 
# 
# VT State Grids
# Work this state's primary grids (w/any US station in the grid): FN32 FN33
# FN34 FN44
# 
# 
# WA State Grids
# Work this state's primary grids (w/any US station in the grid): CN85 CN86
# CN87 CN88 CN95 CN96 CN97 CN98 DN05 DN06 DN07 DN08 DN16 DN17 DN18
# 
# 
# WI State Grids
# Work this state's primary grids (w/any US station in the grid): EN34 EN35
# EN36 EN42 EN43 EN44 EN45 EN46 EN52 EN53 EN54 EN55 EN56 EN65
# 
# 
# WV State Grids
# Work this state's primary grids (w/any US station in the grid): EM87 EM88
# EM97 EM98 EM99 EN90 FM08 FM09 FM19
# 
# 
# WY State Grids
# Work this state's primary grids (w/any US station in the grid): DN41 DN42
# DN43 DN44 DN51 DN52 DN53 DN54 DN61 DN62 DN63 DN64 DN71 DN72 DN73 DN74
# 
# 
# WALC-NA
# Work the Left Coast of North America and earn the WALC-NA endorsement! To
# qualify for the WALC-NA, work Alaska, British Columbia, Washington, Oregon
# and California on PSK31, one contact required in each state/province for a
# total of 5 contacts. Valid contacts are those made after 16 March 2009, 160M
# thru 6M only.
 
 
# Endorsements for contacts from Around the World
# 
# 2019 Christmas Run
# Work 25 PSK-31 QSOs on December 25th 2019 UTC
# Expires 2019-12-31
# 
# 24x7
# 
# 24x7 [072]
# Work each of the 168 (24*7) day-of-week-hour slots.
# 
# 365
# 
# Clock and Calendar
# Complete the entire 24x7 and 365+1 challenges.
# 
# Leap Year
# Work a contact on Feb 29th of any year.
# 
# 365 [090]
# Work all 366 different calendar days, starting 2016-01-01.
# 
# 365 [180]
# 
# 365 [270]
# 
# 365 [360]
# 
# 365 [365]
# 
# 365 [366]
 
# Antarctica
# Work the Antarctica continent starting 2014-09-01.
 
# DX-Specials
# 
# 2019DX-I (Italy)
# Italy is a DX Special for 2019. To qualify for the endorsement, work 20
# different stations on PSK31 mode that are operating from within the specified
# entity during the calendar year.  Expires 2020-01-31
# 
# 2019DX-KH (Hawaii)
# Hawaii is a DX Special for 2019. To qualify for the endorsement, work 20
# different stations on PSK31 mode that are operating from within the specified
# entity during the calendar year.  Expires 2020-01-31
# 
# 2019DX-XE (Mexico)
# Mexico is a DX Special for 2019. To qualify for the endorsement, work 20
# different stations on PSK31 mode that are operating from within the specified
# entity during the calendar year.  Expires 2020-01-31
 
 
# IOTA
# 
# IOTA [10]
# Your goal is to work 250 different IOTA entities using PSK31 mode on the hf
# bands, 160 thru 6m. All contactsmust be made after 31 Dec 2008UTC. This
# endorsement is available in increments of 10, up to 250 entities worked.
# Addendum: A member who activates an IOTA entity will get credit for that
# entity, provided that at least one (1) PSK31 contact is made from that
# entity. This addendum is effective 01 Jan 2012 and will remain in effect for
# the duration of the IOTA endorsement. To apply, use the Online Endorsement
# Checker, and be sure that your logger is providing the IOTA adif field with
# proper RSGB IOTA values.
# 
# IOTA [20]
# IOTA [30]
# IOTA [40]
# IOTA [50]
# IOTA [60]
# IOTA [70]
# IOTA [80]
# IOTA [90]
# IOTA [100]
# IOTA [110]
# IOTA [120]
# IOTA [130]
# IOTA [140]
# IOTA [150]
# IOTA [160]
# IOTA [170]
# IOTA [180]
# IOTA [190]
# IOTA [200]
# IOTA [210]
# IOTA [220]
# IOTA [230]
# IOTA [240]
# IOTA [250]


# PSK GOLF
# 
# PSK GOLF [9]
# For PSK Golf, the earth is divided into 18 "holes" where each hole is 18
# major grid squares. PSK31 contacts on or after 2003-11-03 qualify.
# 
# PSK GOLF [18]
# For PSK Golf, the earth is divided into 18 "holes" where each hole is 18
# major grid squares. PSK31 contacts on or after 2003-11-03 qualify.


# RCC
# 
# Ragchewers 3/30
# Work at least three 30 minute or longer QSOs to become an official 070 Club
# Ragchewer!
 
 
# TRI-WARC
# 
# TRI-WARC
# To stimulate PSK31 on the WARC bands, the 070 Club offers the "TRI-WARC"
# pennant. Work three different stations on each of the WARC bands (30M, 17M
# and 12M) for a total of 9 contacts. Log info only required. Valid contacts
# are those made after 4 July 2001.
# 
# 12/12M
# For the WARCsters out there who have earned the TRI-WARC pennant (REQUIRED),
# work 12 different PSK31 stations total on 12M. Valid contacts are those made
# after 4 July 2001.
# 
# 17/17M
# For the WARCsters out there who have earned the TRI-WARC pennant (REQUIRED),
# work 17 different PSK31 stations total on 17M. Valid contacts are those made
# after 4 July 2001.
# 
# 30/30M
# For the WARCsters out there who have earned the TRI-WARC pennant (REQUIRED),
# work 30 different PSK31 stations total on 30M. Valid contacts are those made
# after 4 July 2001.


# Top Band
# 
# Top Band
# "Top Band" - Work 20 different stations on 160M using PSK31 mode to qualify
# for the Top Band endorsement. Valid contacts are those made on or after 01
# January 2012.
# 
# WAC
# Work each of the six ham radio world continents (EU, AF, AS, NA, SA and OC)
# on PSK31 and you qualify for the "WAC" endorsement. Use the current ARRL DXCC
# country list for reference.


if __name__ == '__main__':
    import adifparser
    import argparse
    import pprint

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('inputfile', metavar='ADIF')
    args = parser.parse_args()

    records = adifparser.parse(args.inputfile)

    print("checking endorsements in {}".format(args.inputfile))
    print("===== Aloha =====")
    aloha = aloha(records)
    if aloha != None:
        print("\tAloha - PASS: <CALL:{}>{} <BAND:{}>{} <QSO_DATE:{}>{} <TIME_ON:{}>{} <MODE:{}>{}"
            .format(  
                aloha['call']['length'],
                aloha['call']['data'],
                aloha['band']['length'],
                aloha['band']['data'],
                aloha['qso_date']['length'],
                aloha['qso_date']['data'],
                aloha['time_on']['length'],
                aloha['time_on']['data'],
                aloha['mode']['length'],
                aloha['mode']['data'],
            )
        )
    else:
        print("\tAloha - FAIL: No Aloha for you :-( ")

    print("===== China Clipper =====")
    found,missing = china_clipper(records)
    print("     ===== Found =====")
    if len(missing) < 5:
        for key in found.keys():
            try:
                print("\tChina Clipper {} - PASS: <CALL:{}>{} <BAND:{}>{} <QSO_DATE:{}>{} <TIME_ON:{}>{} <MODE:{}>{}"
                    .format(  
                        key,
                        found[key]['call']['length'],
                        found[key]['call']['data'],
                        found[key]['band']['length'],
                        found[key]['band']['data'],
                        found[key]['qso_date']['length'],
                        found[key]['qso_date']['data'],
                        found[key]['time_on']['length'],
                        found[key]['time_on']['data'],
                        found[key]['mode']['length'],
                        found[key]['mode']['data'],
                    )
                )
            except:
                print("\tERROR: {} : {} ".format (key,found[key]))
    else:
        print("\tChina Clipper - FAIL: Not complete :-( ")
    if len(missing) != 0:
        print("    ===== Missing =====")
        for key in missing.keys():
            print("\tChina Clipper {} - FAIL: {} : {}".format(key, key, missing[key]))
