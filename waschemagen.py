#Azure Web Apps loWgs schema generator. Creates both external table and set of partitions
#Usage: weblogschemagen.py [table] [HDFS directory] [HQL script name]

import argparse, os

#reading and validating input arguments
parser = argparse.ArgumentParser(description="Azure Web Apps log Hive schema generator.")
parser.add_argument('table', type=str, help='name of the hive table')
parser.add_argument('directory', type=str, help='name of HDFS directory (may be wasb://...)')
parser.add_argument('script', type=str, help='name of generated script file')
parser.add_argument('-v', help="verbose-prints some useful information", action="store_true")
args = parser.parse_args()

#reading HDFS directory structure
if args.v:
    print "Reading HDFS structure"
cmd = "hdfs dfs -ls -R %s > dirstructure.tmp" % args.directory
os.system(cmd)

#parsing directory structure
table = args.table
dirstructfile = file("dirstructure.tmp")

scriptfile = file(args.script, "w")
if args.v:
    print "Generating script..."
scriptfile.write("""
    DROP TABLE %s;
    CREATE EXTERNAL TABLE %s (
    date string,
    time  string,
    ssitename string,
    csmethod  string,
    csuristem  string,
    csuriquery string,
    sport int,
    csusername string,
    cip string,
    UserAgent string,
    Cookie string,
    Referer string,
    cshost string,
    scstatus string,
    scsubstatus string,
    scwin32status string,
    scbytes int,
    csbytes int,
    timetaken int)
    COMMENT 'Azure web site log analytics'
    PARTITIONED BY (Year int, Month int, Day int, Hour int)
    ROW FORMAT DELIMITED FIELDS TERMINATED BY ' ' TBLPROPERTIES("skip.header.line.count"="2");
    """ % (table, table))

partitions = {}
for line in dirstructfile:
    filepath = line.split()[-1]
    if filepath.endswith(".log"):
        filepath= filepath.split("/")[:-1]
        partitions['/'.join(filepath)] = filepath[-4:]
    
dirstructfile.close()


for p in partitions:
    scriptfile.write("ALTER TABLE %s ADD IF NOT EXISTS PARTITION(Year=%s, Month=%s, Day=%s, Hour=%s) LOCATION '%s';\n" % (table, partitions[p][0], partitions[p][1], partitions[p][2], partitions[p][3], p))

scriptfile.close()
if args.v:
    print('Job completed. %s partitions identified.' % len(partitions))
os.remove("dirstructure.tmp")
