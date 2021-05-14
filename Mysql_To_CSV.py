import mysql.connector
from mysql.connector import errors
import time
import progressbar
from pathlib import Path

total_time = 0


# conversion from list to string
def list_to_string(string):
    li = list(string.split(", "))
    return li


# taking tables
def user_input():
    print("\nInsert your tabs, separated by a ,\n")
    inp_tabs = str(input())
    tables = list_to_string(inp_tabs)
    return tables


# self-explanatory
def check_connection(path):
    if Path(path).is_file():
        try:
            # Reading db's connection parameters
            my_file = open(path, "r")
            content_list = my_file.read().split(",")
            my_file.close()
            # Connecting to the db
            cnx = mysql.connector.connect(
                host=content_list[0],
                user=content_list[1],
                password=content_list[2],
                database=content_list[3],
                auth_plugin='mysql_native_password'
            )
            print("\nConnected to the db")
            return cnx
        except errors:
            print("Login failed ", errors)
    else:
        print("File not exist")


def export(cnx, tables):
    # Variables
    localtime = time.asctime(time.localtime(time.time()))
    global total_time
    table_rows = 0

    # cursor creation + query
    cursor = cnx.cursor()
    cursor.execute('select * from ' + tables)

    # fetch all rows' numbers + query + header's list
    print("\nCounting all " + tables + " rows\n")
    while True:
        rows = cursor.fetchmany(1000000)
        if len(rows) == 0:
            break
        else:
            table_rows += len(rows)
            print(table_rows, " rows ")
    print("\nAll " + tables + " rows: ", table_rows)
    cursor.execute('select * from ' + tables)
    header = [row[0] for row in cursor.description]

    # .csv files creation (exported tab, stats)
    print("\nCreating tab .csv file")  # debug
    f = open(tables + '.csv', 'w')

    # Write header
    f.write(','.join(header) + '\n')

    # Start time
    start = time.time()
    print("\nStart exporting " + tables + "\n")

    for j in progressbar.progressbar(range(table_rows)):
        # all tab's elements
        all_rows = 0
        while True:
            rows = cursor.fetchmany(100000)
            if len(rows) == 0:
                break
            else:
                for row in rows:
                    f.write(','.join(str(r) for r in row) + '\n')
            all_rows += int(str(len(rows)))

    # Closing connection
    cnx.close()

    # Closing export tab's file
    f.close()

    # End time
    end = time.time()

    # Debugs + relative + absolute time values
    print('\nTotal rows added:', table_rows)
    print("\nRelative export time: " + "%.2f" % float((end - start) / 60) + " minutes")
    rel_time = float((end - start) / 60)
    tab_time = "\n" + localtime + "\nTable name: " + tables + "\nRows: " + str(
        table_rows) + "\nTotal export time: " + "%.2f" % float(
        (end - start) / 60) + " minutes\n\n"
    tab_time_csv = "\n" + localtime + ", " + tables + ", " + str(table_rows) + ", " + "%.2f" % float(
        (end - start) / 60)
    total_time += rel_time
    print("\nTotal export time: " + "%.2f" % float(total_time) + " minutes")
    return tab_time, tab_time_csv, total_time


def write_to_csv(tab_time, tab_time_csv, total_time):
    # Opening files
    stats = open('stats_files.txt', 'a')
    stats_csv = open('stats_files_csv.csv', 'a')

    # Writing to files
    stats.write(str(tab_time))
    #
    stats_csv.write(str(tab_time_csv))

    # Closing files
    stats.close()
    stats_csv.close()


########################################################################
############                   DEBUG                       #############
########################################################################

if __name__ == '__main__':
    tabs = user_input()
    print("\nPefect! Now add db_configuration filepath\n")
    config_path = str(input())
    for i in tabs:
        conn = check_connection(config_path)
        tab_time, tab_time_csv, total_time = export(conn, i)
        write_to_csv(tab_time, tab_time_csv, total_time)

    stats = open('stats_files.txt', 'a')
    stats.write("\nTotal time: " + "%.2f" % float(
        total_time) + " minutes" + "\n\n" + "#######################################" + "\n\n")
    stats.close()
