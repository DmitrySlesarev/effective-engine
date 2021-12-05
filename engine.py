#!/usr/bin/python3
#-*-coding:utf-8-*-

import os
import sys
import pandas as pd
import xml.etree.ElementTree as ET

log = sys.argv[1]  # amari.log
xml = sys.argv[2]  # example.xml

scenario = '    *** TEST CASE #3: OVERALL RRC MESSAGING VERIFICATION ***'

wishlist = dict(MIB='configMIB.xml',
                SIB1='configSIB1.xml',
                SIB2='configSIB2.xml',)

givenlist = dict(MIB='liveMIB.txt',
                 SIB1='liveSIB1.txt',
                 SIB2='liveSIB2.txt',)

mib3GPP = {'systemFrameNumber-MSB-r13': None,
           'hyperSFN-LSB-r13': None,
           'schedulingInfoSIB1-r13': '2',
           'systemInfoValueTag-r13': '0',
           'ab-Enabled-r13': False,
           'operationModeInfo-r13': None,
           'inband-SamePCI-r13': None,
           'eutra-CRS-SequenceInfo-r13': None,
           'spare': None}

sib13GPP = {'hyperSFN-MSB-r13': None,
            'cellAccessRelatedInfo-r13': None,
            'plmn-IdentityList-r13': None,
            'plmn-Identity-r13': None,
            'mcc': 2,
            'mnc': 0,
            'cellReservedForOperatorUse-r13': False,
            'attachWithoutPDN-Connectivity-r13': True,
            'trackingAreaCode-r13': None,
            'cellIdentity-r13': 0,
            'cellBarred-r13': "notBarred",
            'intraFreqReselection-r13': 'notAllowed',
            'cellSelectionInfo-r13': None,
            'q-RxLevMin-r13': -70,
            'q-QualMin-r13': -20,
            'p-Max-r13': None,
            'freqBandIndicator-r13': '28',
            'freqBandInfo-r13': None,
            'multiBandInfoList-r13': None,
            'downlinkBitmap-r13': None,
            'eutraControlRegionSize-r13': 'n2',
            'nrs-CRS-PowerOffset-r13': 'dB0',
            'schedulingInfoList-r13': 0,
            'si-WindowLength-r13': 'ms160',
            'si-RadioFrameOffset-r13': None,
            'systemInfoValueTagList-r13': None,
            'nonCriticalExtension': None,
            }

sib23GPP = {'radioResourceConfigCommon-r13': None,
             'ue-TimersAndConstants-r13': None,
             't300-r13': 'ms10000',
             't301-r13': 'ms10000',
             't310-r13': 'ms1000',
             'n310-r13': 'n2',
             't311-r13': 'ms1000',
             'n311-r13': 'n1',
             'freqInfo-r13 SEQUENCE': None,
             'ul-CarrierFreq-r13': None,
             'additionalSpectrumEmission-r13': 1,
             'timeAlignmentTimerCommon-r13': 'sf750',
             'multiBandInfoList-r13': None,
             'ateNonCriticalExtension': None,
             'cellReselectionInfoCommon-r13': None,
             'q-Hyst-r13': None,
             'cellReselectionServingFreqInfo': None,
             's-NonIntraSearch-r13': None,
             'intraFreqCellReselectionInfo-r13': None,
             'q-RxLevMin-r13': -70,
             'q-QualMin-r13': None,
             'p-Max-r13': None,
             's-IntraSearchP-r13': None,
             't-Reselection-r13': None,
             'freqBandInfo-r13': None,
             'multiBandInfoList-r1': None,
             'lateNonCriticalExtension': None,
}

def main():
    #clean workspace
    try:
        for key in wishlist:
            os.remove(os.path.join(os.path.abspath(os.path.dirname(file)), wishlist[key]))
        for key in givenlist:
            os.remove(os.path.join(os.path.abspath(os.path.dirname(file)), givenlist[key]))
    except FileNotFoundError:
        print("No obsolete files in working directory.")
    finally:
        pass


def prepareFiles(file):

    global wishlist

    hdr = '[NB IoT]'
    endline = '</BCCH'

    def separate_file(delimeter, line, f, hdr, endline, filename):
        if delimeter in line:
            with open(filename, 'a+') as working:
                while True:
                    line = f.readline()
                    if hdr not in line:
                        working.write(line)
                    if endline in line:
                        break

    with open(file) as f:

        while True:
            line = f.readline()
            if not line:
                breaka
for key in wishlist:
                separate_file(key, line, f, hdr, endline, wishlist[key])

def parseXML(file):

    MIB = dict()
    SIB1 = dict()
    SIB2 = dict()

    events = ("start", "start-ns")

    if file == 'configMIB.xml':
        for event, elem in ET.iterparse(file, events=events):
            try:
                #print(elem.tag, elem.text.strip())
                MIB[elem.tag] = elem.text.strip()
            except AttributeError:
                #print(elem.tag, None)
                MIB[elem.tag] = None
        return MIB

    if file == 'configSIB1.xml':
        count = 0
        for event, elem in ET.iterparse(file, events=events):
            try:
                #crutch for IE 'MCC-MNC-Digit'
                if elem.tag == 'MCC-MNC-Digit':
                    SIB1[elem.tag + str(count)] = elem.text.strip()
                    count += 1
                else:
                    SIB1[elem.tag] = elem.text.strip()
            except AttributeError:
                SIB1[elem.tag] = None
        return SIB1

    if file == 'configSIB2.xml':
        for event, elem in ET.iterparse(file, events=events):
            try:
                SIB2[elem.tag] = elem.text.strip()
            except AttributeError:
                SIB2[elem.tag] = None
        return SIB2

    # clean the memory
    for event, elem in ET.iterparse(file, events=events):
        if elem.tag == "record_tag" and event == "end":
            elem.clear()


def parseTXT(file):

    delimeter = '[RRC] DL 0001 d001 BCCH-NB: SIB'
    startline = '[RRC] DL 0001 d001 BCCH-NB: SIB'
    sidechar = ["{", "}", ",", ":"]

    MIB = dict()
    SIB1 = dict()
    SIB2 = dict()

    count = 0

    def separate_file(delimeter, line, f, sidechar, SI, filename):
        if delimeter in line:
            with open(filename, 'a+') as working:
                while True:
                    line = f.readline()
                    endline = line
                    for i in sidechar:
                        line = line.replace(i, '')
                        line = line.strip(' ')
                    if line.isspace():
                        pass
                    else:
                        working.write(line)
                        try:
                            SI[line.split()[0]] = line.split()[1]
                        except IndexError:
                            SI[line.split()[0]] = None
                        if endline.isspace():
                            break
        return SI

    with open(file) as f:
        while True:
            line = f.readline()
            if not line:
                count += 1
                if count > 3:
                    break
                continue

            if '[PHY] DL 0001 00    -     - NPBCH' in line:
                with open('liveMIB.txt', 'a+') as working:
                    working.write(line)
                    line = line.split()
                    for i in line:
                        if len(i) < 5:
                            pass
                        else:
                            if 'sched_info_sib1=' in i:
                                MIB['schedulingInfoSIB1-r13'] = i[-1::]
                            if 'si_value_tag=0' in i:
                                MIB['systemInfoValueTag-r13'] = i[-1::]
                            if 'ab_enabled=0' in i:
                                MIB['ab-Enabled-r13'] = i[-1::]
                            if 'op_mode=3' in i:
                                MIB['operationModeInfo-r13'] = i[-1::]
if '[RRC] DL 0001 00 BCCH-NB: SIB1' in line:
                with open('liveSIB1.txt', 'a+') as working:
                    while True:
                        line = f.readline()
                        endline = line
                        for i in sidechar:
                            line = line.replace(i, "")
                            line = line.strip(' ')
                        if line.isspace():
                            pass
                        else:
                            working.write(line)
                            try:
                                SIB1[line.split()[0]] = line.split()[1]
                            except IndexError:
                                SIB1[line.split()[0]] = None
                        if endline.isspace():
                            break

            if '[RRC] DL 0001 d001 BCCH-NB: SIB' in line:
                with open('liveSIB2.txt', 'a+') as working:
                    while True:
                        line = f.readline()
                        endline = line
                        for i in sidechar:
                            line = line.replace(i, "")
                            line = line.strip(' ')
                        if line.isspace():
                            pass
                        else:
                            working.write(line)
                            try:
                                SIB2[line.split()[0]] = line.split()[1]
                            except IndexError:
                                SIB2[line.split()[0]] = None
                        if endline.isspace():
                            break

            count = 0

    return MIB, SIB1, SIB2

def compareDict(source, destination):
    d1_keys = set(source.keys())
    d2_keys = set(destination.keys())
    shared_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    modified = {o : (source[o], destination[o]) for o in shared_keys if source[o] != destination[o]}
    same = set(o for o in shared_keys if source[o] == destination[o])
    return added, removed, modified, same

def crutchBroadcastingMIB(yourDict):
    #overall crutch
    for key in yourDict.keys():
        if yourDict[key] == '':
            yourDict[key] = None
    #crutch MIB
    if 'BCCH-BCH-Message-NB' in yourDict.keys():
        yourDict.pop('BCCH-BCH-Message-NB')
    if 'message' in yourDict.keys():
        yourDict.pop('message')
    if 'false' in yourDict.keys():
        yourDict['ab-Enabled-r13'] = False
        yourDict.pop('false')
    elif 'true' in yourDict.keys():
        yourDict['ab-Enabled-r13'] = True
        yourDict.pop('true')
    return yourDict
if '[RRC] DL 0001 00 BCCH-NB: SIB1' in line:
                with open('liveSIB1.txt', 'a+') as working:
                    while True:
                        line = f.readline()
                        endline = line
                        for i in sidechar:
                            line = line.replace(i, "")
                            line = line.strip(' ')
                        if line.isspace():
                            pass
                        else:
                            working.write(line)
                            try:
                                SIB1[line.split()[0]] = line.split()[1]
                            except IndexError:
                                SIB1[line.split()[0]] = None
                        if endline.isspace():
                            break

            if '[RRC] DL 0001 d001 BCCH-NB: SIB' in line:
                with open('liveSIB2.txt', 'a+') as working:
                    while True:
                        line = f.readline()
                        endline = line
                        for i in sidechar:
                            line = line.replace(i, "")
                            line = line.strip(' ')
                        if line.isspace():
                            pass
                        else:
                            working.write(line)
                            try:
                                SIB2[line.split()[0]] = line.split()[1]
                            except IndexError:
                                SIB2[line.split()[0]] = None
                        if endline.isspace():
                            break

            count = 0

    return MIB, SIB1, SIB2

def compareDict(source, destination):
    d1_keys = set(source.keys())
    d2_keys = set(destination.keys())
    shared_keys = d1_keys.intersection(d2_keys)
    added = d1_keys - d2_keys
    removed = d2_keys - d1_keys
    modified = {o : (source[o], destination[o]) for o in shared_keys if source[o] != destination[o]}
    same = set(o for o in shared_keys if source[o] == destination[o])
    return added, removed, modified, same

def crutchBroadcastingMIB(yourDict):
    #overall crutch
    for key in yourDict.keys():
        if yourDict[key] == '':
            yourDict[key] = None
    #crutch MIB
    if 'BCCH-BCH-Message-NB' in yourDict.keys():
        yourDict.pop('BCCH-BCH-Message-NB')
    if 'message' in yourDict.keys():
        yourDict.pop('message')
    if 'false' in yourDict.keys():
        yourDict['ab-Enabled-r13'] = False
        yourDict.pop('false')
    elif 'true' in yourDict.keys():
        yourDict['ab-Enabled-r13'] = True
        yourDict.pop('true')
    return yourDict     

def crutchBroadcastingSIB1(yourDict):
    #overall crutch
    for key in yourDict.keys():
        if yourDict[key] == '':
            yourDict[key] = None
    #crutch SIB1
    if 'BCCH-DL-SCH-Message-NB' in yourDict.keys():
        yourDict.pop('BCCH-DL-SCH-Message-NB')
    if 'message' in yourDict.keys():
        yourDict.pop('message')
    if 'c1' in yourDict.keys():
        yourDict.pop('c1')
    if 'notReserved' in yourDict.keys():
        yourDict.pop('notReserved')
        yourDict['cellReservedForOperatorUse-r13'] = 'notReserved'
    if 'true' in yourDict.keys():
        yourDict.pop('true')
        yourDict['attachWithoutPDN-Connectivity-r13'] = True
    elif 'false' in yourDict.keys():
        yourDict.pop('false')
        yourDict['attachWithoutPDN-Connectivity-r13'] = False
    if 'notBarred' in yourDict.keys():
        yourDict.pop('notBarred')
        yourDict['cellBarred-r13'] = 'notBarred'
    elif 'Barred' in yourDict.keys():
        yourDict.pop('Barred')
        yourDict['cellBarred-r13'] = 'Barred'
    if 'notAllowed' in yourDict.keys():
        yourDict.pop('notAllowed')
        yourDict['intraFreqReselection-r13'] = 'notAllowed'
    elif 'Allowed' in yourDict.keys():
        yourDict.pop('Allowed')
        yourDict['intraFreqReselection-r13'] = 'Allowed'
    if 'n3' in yourDict.keys():
        yourDict.pop('n3')
        yourDict['eutraControlRegionSize-r13'] = 'n3'
    else:
        yourDict['eutraControlRegionSize-r13'] = 'WARNING'
    if 'db0' in yourDict.keys():
        yourDict.pop('db0')
        yourDict['nrs-CRS-PowerOffset-r13'] = 'db0'
    return yourDict

#main
if name == 'main':
    main()

    print("\n"*3) # replace this with decorator
    print(scenario, "\n")

    prepareFiles(xml)

    mibXML = parseXML('configMIB.xml')
    sib1XML = parseXML('configSIB1.xml')
    sib2XML = parseXML('configSIB2.xml')

    correctedMIB = crutchBroadcastingMIB(mibXML)
    correctedSIB1 = crutchBroadcastingSIB1(sib1XML)
    for i in correctedSIB1.keys():
        print(i, correctedSIB1[i])
    added, removed, modified, same = compareDict(mib3GPP, mibXML)

#    print("*** MIB items as per 3GPP TS 36.508 version 13.2.0 Release 13 Table 8.1.4.3.2-1 ***\nAdded:", added)
#    print("Modified:")
#    for key in modified:
#        print(key, modified[key])
#    print("Removed:", removed, "\nSame:", same)
#
#    added, removed, modified, same = compareDict(sib13GPP, sib1XML)
#    print("*** SIB1 items as per 3GPP TS 36.508 version 13.2.0 Release 13 Table 8.1.4.3.2-3 ***\nAdded:", added,
#          "\nRemoved:", removed, "\nModified:", modified, "\nSame:", same)
#
#    added, removed, modified, same = compareDict(sib23GPP, sib2XML)
#    print("*** SIB2 items as per 3GPP TS 36.508 version 13.2.0 Release 13 Tables 8.1.4.3.3-1 ***\nAdded:", added,
#          "\nRemoved:", removed, "\nModified:", modified, "\nSame:", same)
#
    mibTXT, sib1TXT, sib2TXT = parseTXT(log)
#
#    added, removed, modified, same = compareDict(mibTXT, mibXML)
#    print("\n\n\n*** MIB from Amari log file vs MIB from XML config file ***\nAdded:", added)
#    print("Modified:")
#    for key in modified:
#        print(key, modified[key])
#    print("Removed:", removed, "\nSame:", same)
#
#    added, removed, modified, same = compareDict(sib1TXT, sib1XML)
#    print("*** SIB1 from Amari log file vs MIB from XML config file ***\nAdded:", added,
#          "\nRemoved:", removed, "\nModified:", modified, "\nSame:", same)
#
#    added, removed, modified, same = compareDict(sib2TXT, sib2XML)
#    print("*** SIB2 from Amari log file vs MIB from XML config file ***\nAdded:", added,
#          "\nRemoved:", removed, "\nModified:", modified, "\nSame:", same)

    #display MIB
    xml = []
    for i in mib3GPP.keys():
        if i in correctedMIB:#if i in mibXML:
            xml.append(correctedMIB[i])#xml.append(mibXML[i])
        else:
            xml.append("MISSING")

    amari = []
    for i in mib3GPP.keys():
        if i in mibTXT.keys():
            amari.append(mibTXT[i])
        else:
            amari.append('MISSING')

verdict = []
    for i in range(len(mib3GPP.keys())):
        if xml[i] == amari[i]:
            verdict.append('PASS')
        else:
            verdict.append('FAIL')

    print("="*66) # replace this with decorator
    print("\t\t\t\tMIB")
    print("=" * 66)
    df_mib = pd.DataFrame({'IE': [key for key in mib3GPP.keys()],
                           '3GPP': [value for value in mib3GPP.values()],
                           'XML': [ie for ie in xml],
                           'Amari': [ie for ie in amari],
                           'Verdict': [ie for ie in verdict] })
    print(df_mib)
    print("="*66)
    print('SUMMARY:' + '.'*(66-4-8) + 'FAIL' if 'FAIL' in verdict else 'PASS')
    print("\n")

    #display SIB1
    xml = []
    for i in sib13GPP.keys():
        if i in sib1XML:
            xml.append(sib1XML[i])
        else:
            xml.append('MISSING')

    amari = []
    for i in sib13GPP.keys():
        if i in sib1TXT.keys():
            amari.append(sib1TXT[i])
        else:
            amari.append('MISSING')

    verdict = []
    for i in range(len(sib13GPP.keys())):
        if xml[i] == amari[i]:
            verdict.append('PASS')
        else:
            verdict.append('FAIL')

    print("="*100) # replace this with decorator
    print("\t\t\t\t\t\tSIB1")
    print("=" * 100)
    df_sib1 = pd.DataFrame({'IE': [key for key in sib13GPP.keys()],
                           '3GPP': [value for value in sib13GPP.values()],
                           'XML': [ie for ie in xml],
                            'Amari': [ie for ie in amari],
                           'Verdict': [ie for ie in verdict]})
    print(df_sib1)
    print("="*100)
    print('SUMMARY:' + '.'*(100-4-8) + 'FAIL' if 'FAIL' in verdict else 'PASS')
    print("\n")

    #display SIB2
    xml = []
    for i in sib23GPP.keys():
        if i in sib2XML:
            xml.append(sib2XML[i])
        else:
            xml.append('MISSING')

    amari = []
    for i in sib23GPP.keys():
        if i in sib2TXT.keys():
            amari.append(sib2TXT[i])
        else:
            amari.append('MISSING')

    verdict = []
    for i in range(len(sib23GPP.keys())):
        if xml[i] == amari[i]:
            verdict.append('PASS')
        else:
            verdict.append('FAIL')

    print("="*72) # replace this with decorator
    print("\t\t\t\tSIB2")
    print("=" * 72)
    df_sib2 = pd.DataFrame({'IE': [key for key in sib23GPP.keys()],
                           '3GPP': [value for value in sib23GPP.values()],
                            'XML': [ie for ie in xml],
                            'Amari': [ie for ie in amari],
                            'Verdict': [ie for ie in verdict]})
    print(df_sib2)
    print("="*72)
    print('SUMMARY:' + '.'*(72-4-8) + 'FAIL' if 'FAIL' in verdict else 'PASS')
    print("\n")
