import csv
from time import time

hist_file = 'history.csv'


def read_csv():
    rows = []
    # try opening in read mode. if it fails, create the file
    try:
        with open(hist_file, 'r'):
            pass
    except (FileNotFoundError):
        with open(hist_file, 'w+'):
            print(f"{hist_file} does not exist, creating it")
            pass
    with open(hist_file, 'r', newline='') as csvfile:
        myreader = csv.reader(csvfile, delimiter=',')
        next(myreader, None)  # skip header
        for row in myreader:
            if [col for col in row if col == ''] or len(row) != 3:
                # skip row if there's less than 3 cols or col is empty
                # avoids IndexError in plot_grapy.py
                print("incomplete row, skipped")
                continue
            rows.append(row)
    return rows


def remove_old_rows(rows, max_age):
    max_age = max_age * 60
    current_time = int(time())
    clean_rows = []
    for row in rows:
        if int(row[0]) + max_age > current_time:
            clean_rows.append(row)
    return clean_rows


def write_csv(timestamp, date, temp, max_rows=None, max_age=None):
    header = ["timestamp", "date", "temp"]
    rows = read_csv()
    rows.append([timestamp, date, temp])  # append most recent reading
    if max_rows is not None and len(rows) > max_rows:
        # remove oldest reading
        rows.pop(0)
    if max_age is not None:
        # remove entries older than max_age minutes
        rows = remove_old_rows(rows, max_age)
    with open(hist_file, 'w', newline='') as csvfile:
        mywriter = csv.writer(csvfile, delimiter=',')
        mywriter.writerow(header)
        for row in rows:
            # print(row)
            mywriter.writerow(row)


if __name__ == "__main__":
    from os import system
    start = time()
    write_csv(int(start),"is","a test", None, 10)
    end = time()
    row_count = len(read_csv())
    print(f'wrote {row_count} rows in {end - start} seconds')
    # remove the last line
    system(f"lines=$(head -n-1 {hist_file}); echo \"$lines\" > {hist_file}")
