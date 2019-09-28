import csv
import sys
import os.path


def ParseCSVFile(fileName, fileID, fileDelimiter):
    returnValues = []
    if fileID == "--messages":
        fType = "PRN"
    elif fileID == "--tracer":
        fType = "TBT"
    else:
        fType = "UNK"
    with open(fileName) as csvfile:
        reader = csv.reader(csvfile, delimiter=fileDelimiter)
        for row in reader:
            if len(row) > 5:
                returnValues.append({
                    'SRC': fType,
                    'SEV': row[0],
                    'DATE': row[1],
                    'TIME': row[2],
                    'TASK': row[3],
                    'MSG': row[4]+row[5]
                })
    return returnValues


def sortByTime(listToSort):
    return listToSort['TIME']

# Process command line arguments for messages and tracer files
argsOk = True

if len(sys.argv) < 2:
    argsOk = False
else:
    arg1 = sys.argv[1].split("=")
    arg2 = sys.argv[2].split("=")
    argsOk = (arg1[0] == "--messages" and arg2[0] == "--tracer")
    argsOk = argsOk or (arg2[0] == "--messages" and arg1[0] == "--tracer")

if argsOk is False:
    print("Syntax error: logfilemerge.py --messages=messageFilename \
    --tracer=tracerFilename")
    exit(0)

if not(os.path.isfile(arg1[1])):
    print("File not available: "+arg1[1])
    exit(0)

if not(os.path.isfile(arg2[1])):
    print("File not available: "+arg2[1])
    exit(0)

file1 = ParseCSVFile(
    arg1[1],
    arg1[0],
    ";")

file2 = ParseCSVFile(
    arg2[1],
    arg2[0],
    ";")

allMessages = []
allMessages = file1 + file2

allMessages.sort(key=sortByTime)

for row in allMessages:
    print(
        row['SEV'].strip(),
        row['DATE'].strip(),
        row['TIME'].strip(),
        row['SRC'].strip(),
        row['TASK'].strip(),
        row['MSG'].strip(),
        sep=";")
