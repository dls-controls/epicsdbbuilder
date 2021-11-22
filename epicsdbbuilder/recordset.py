'''Collections of records.'''

from __future__ import print_function

import os
import time

__all__ = [
    'WriteRecords', 'Disclaimer',
    'LookupRecord', 'CountRecords', 'ResetRecords']


class RecordSet(object):
    def ResetRecords(self):
        self.__RecordSet = {}
        self.__HeaderLines = []
        self.__BodyLines = []

    def __init__(self):
        self.ResetRecords()

    # Add a record to the list of records to be published.
    def PublishRecord(self, name, record):
        assert name not in self.__RecordSet, 'Record %s already defined' % name
        self.__RecordSet[name] = record

    # Returns the record with the given name.
    def LookupRecord(self, full_name):
        return self.__RecordSet[full_name]

    # Output complete set of records to the given file.
    def Print(self, output, alphabetical):
        for line in self.__HeaderLines:
            print(line, file = output)
        if self.__BodyLines:
            print(file = output)
            for line in self.__BodyLines:
                print(line, file = output)
        # Print the records in alphabetical order: gives the reader a fighting
        # chance to find their way around the generated database!
        sort = sorted if alphabetical else list
        for record in sort(self.__RecordSet):
            self.__RecordSet[record].Print(output, alphabetical)

    # Returns the number of published records.
    def CountRecords(self):
        return len(self.__RecordSet)

    def AddHeaderLine(self, line):
        self.__HeaderLines.append(line)

    def AddBodyLine(self, line):
        self.__BodyLines.append(line)


recordset = RecordSet()

LookupRecord = recordset.LookupRecord
CountRecords = recordset.CountRecords
ResetRecords = recordset.ResetRecords



def Disclaimer(source = None, normalise_source = True):
    if source is None:
        from_source = '.'
    else:
        if normalise_source:
            source = os.path.abspath(source)
        from_source = ' from\nsource: %s' % source

    now = time.strftime('%a %d %b %Y %H:%M:%S %Z')
    message = '''\
This file was automatically generated on %(now)s%(from_source)s

*** Please do not edit this file: edit the source file instead. ***

''' % locals()
    return message


def WriteRecords(filename, header=None, alphabetical=True):
    if header is None:
        header = Disclaimer()
    header = header.split('\n')
    assert header[-1] == '', 'Terminate header with empty line'
    with open(filename, 'w') as output:
        for line in header[:-1]:
            print('#', line, file = output)
        recordset.Print(output, alphabetical)
