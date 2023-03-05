#!/bin/python3
# Growtopia save.dat decoder

from struct import unpack
import sys


def HELP():
    HELP_TEXT = """
Growotopia save.dat decoder
by Zoxorer

usage: savedat.py <file>

parameter:
    file                                Growotopia save.dat file

example:
    savedat.py save.dat
    """
    print(HELP_TEXT)


def decryptTankidPassword(data):
    res = ""
    for n,char in enumerate(data):
        res += chr(char-(100+n))
    return res

class TypeInvalid(Exception):
    pass


def dump(stream):
    stream.seek(4)
    while True:
        TYPE = unpack("<I", stream.read(4))[0]
        if(TYPE in [1,2,5,9]):
            LENGTH = unpack("<I", stream.read(4))[0]
            KEY = stream.read(LENGTH)
            VALUE = stream.read(4)
            if(TYPE == 5):
                VALUE = unpack("?", VALUE[0].to_bytes(1,"little"))[0]
            elif(TYPE == 1):
                VALUE = unpack("f", VALUE)[0]
            elif(TYPE == 2):
                VALUE_LENGTH = unpack("<i", VALUE)[0]
                VALUE = stream.read(VALUE_LENGTH)
                if(KEY == b"tankid_password"):
                    VALUE = decryptTankidPassword(VALUE)
            elif(TYPE == 9):
                VALUE = unpack("<i",VALUE)[0]
            else:
                raise TypeInvalid("Can't parse type: %s" % (TYPE))
            print("%s : %s" % (KEY.decode(), VALUE))
        elif(TYPE == 0):
            break
        else:
            raise TypeInvalid("Can't parse type: %s" % (TYPE))

if __name__ == "__main__":
    ARGS = sys.argv
    if(len(ARGS) < 2):
        HELP()
        exit()
    try:
        FILE = open(ARGS[1], "rb")
    except Exception as e:
        print("ERROR!",e)
        exit()

    try:
        dump(open(ARGS[1],"rb"))
    except Exception as e:
        print("ERROR!",e)
