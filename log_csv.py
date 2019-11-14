import csv


def read_rows():
    rows = []
    with open('history.csv', 'r', newline='') as csvfile:
        myreader = csv.reader(csvfile, delimiter=',')
        next(myreader, None)  # skip header
        for row in myreader:
            rows.append(row)
    return rows


def write_rows(timestamp, date, temp, max_rows=10):
    header = ["timestamp", "date", "temp"]
    rows = read_rows()
    rows.append([timestamp, date, temp])  # append most recent reading
    if len(rows) > max_rows:
        rows.pop(0)  # remove oldest reading
    with open('history.csv', 'w', newline='') as csvfile:
        mywriter = csv.writer(csvfile, delimiter=',')
        mywriter.writerow(header)
        for row in rows:
            # print(row)
            mywriter.writerow(row)
