import csv

fdts = []
dts = []

with open('falsedt.txt', mode='r') as f:
    falsedt = csv.reader(f, delimiter='　')
    for frow in falsedt:
        fdts.append(frow[2])

with open('budteval.txt', mode='r') as f:
    budteval = csv.reader(f, delimiter='　')
    with open('dtEvaluation.txt', mode='w') as f:
        for row in budteval:
            flg = 1
            for frow in fdts:
                if row[2] == frow:
                    flg = 0
            if flg:
                print(*row, sep='　', file=f)
