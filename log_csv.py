import csv


def read_rows():
    rows = []
    with open('history.csv', 'r', newline='') as csvfile:
        myreader = csv.reader(csvfile, delimiter=',')
        i = 1
        for row in myreader:
            rows.insert(i, row)
            i += 1
    return rows


def write_rows(timestamp, time_str, temp, max_rows=10):
    rows = read_rows()
    rows.insert(0, [timestamp, time_str, temp])  # insert most recent reading
    if len(rows) > max_rows:
        rows.pop(-1)  # remove oldest reading
    with open('history.csv', 'w', newline='') as csvfile:
        mywriter = csv.writer(csvfile, delimiter=',')
        mywriter.writerow(["temestamp", "time_str", "temp"])  # write header
        for row in rows:
            # print(row)
            mywriter.writerow(row)
