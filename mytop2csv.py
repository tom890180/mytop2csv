import sys
import getopt
import subprocess
import re
import time
import signal
import os

def get_mytop_result(index):
    res = subprocess.check_output(['mytop', '-b']).decode('utf-8')

    load = re.search(r'load\ \((.*)\)', res).group(1).split(" ")
    load_one = load[0].replace(".", ",")
    load_five = load[1].replace(".", ",")
    load_fifteen = load[2].replace(".", ",")


    time = re.search(r'up\ (.*)\ \[(.*)]', res)
    up = time.group(1)
    local = time.group(2)

    queries = re.search(r'Queries:\ (.*?)\ ', res).group(1).replace("k", "").replace(".", ",")
    qps = re.search(r'qps:\ \ (.*?)\ ', res).group(1).replace(".", ",")

    slow = re.search(r'Slow:\s*([0-9].[0-9])\ ', res).group(1).replace(".", ",")

    seinupde = re.search(r'Se\/In\/Up\/De\(\%\)\:\s*(.*)\n', res).group(1).split("/")
    select = seinupde[0]
    insert = seinupde[1]
    update = seinupde[2]
    delete = seinupde[3]

    key_efficiency = re.search(r'MyISAM\ Key\ Cache\ Efficiency\:\ (.*)%', res).group(1).replace(".", ",")

    bps = re.search(r'Bps\ in\/out\:\ (.*?)\ ', res).group(1).replace("k", "").split("/")
    bps_in = bps[0].replace(".", ",")
    bps_out = bps[1].replace(".", ",")

    return [str(index), up, local, load_one, load_five, load_fifteen, queries, qps, slow, select, insert, update, delete, key_efficiency, bps_in, bps_out]

def get_csv_headers():
    return ["#", "uptime", "localtime", "load_one", "load_five", "load_fifteen", "total_queries", "qps", "slow", "select", "insert", "update", "delete", "MyISAM_key_efficiency", "bps_in", "bps_out"]

def main(argv):
    output_location = ''
    refresh_rate = 0.2
    opts, args = getopt.getopt(argv,"ho:r:")

    for opt, arg in opts:
        if opt == '-h':
            print('-o <output_location> -r <refresh_rate>')
            sys.exit()
        elif opt in ("-o"):
            output_location = arg
        elif opt in ("-r"):
            refresh_rate = float(arg)


    if output_location == '':
        print("-o <output_location> must be given")
        sys.exit()
    
    print("writing output to {} with refresh rate {}".format(output_location, refresh_rate))

    index = 0

    if os.path.exists(output_location):
        print("{} already exists, quitting".format(output_location))
        sys.exit()

    output_file = open(output_location, "a")

    try:
        output_file.write("\""+"\";\"".join(get_csv_headers())+"\"\n")

        while True:
            output_file.write("\""+"\";\"".join(get_mytop_result(index))+"\"\n")
            output_file.flush()

            index = index + 1
            time.sleep(refresh_rate)
    finally:
        output_file.close()
        print("Write complete")


def handler(signum, frame):
    exit(1)

signal.signal(signal.SIGINT, handler)
    
if __name__ == "__main__":
    main(sys.argv[1:])

