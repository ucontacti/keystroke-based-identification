import csv

def session_number():
    fileObject = csv.reader('data/time.csv')
    row_count = sum(1 for row in fileObject)
    return int(row_count / 5)


def add_to_csv(down, up):
    # Merge down and up data together and add to time.csv
    with open('Modules/data/time.csv', 'a') as fd:
        for s in range(len(down)):
            for i in range(len(down[s])):
                fd.write(str(down[s][i]) + "," + str(up[s][i]))
                if (i != (len(down[s]) - 1)):
                    fd.write(",")
            fd.write("\n")
