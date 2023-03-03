import datetime
import sys

#'01-22-2020 Wed 07:40:25', '%d-%m-%Y %a %H:%M:%S'
if len(sys.argv) > 2:
    print(datetime.datetime.strptime(sys.argv[1], '%m-%d-%Y %a %H:%M:%S').strftime("%Y%m%d%H%M%S000_"+sys.argv[2]))
else:
    print(datetime.datetime.strptime(sys.argv[1], '%m-%d-%Y %a %H:%M:%S').strftime("%Y%m%d%H%M%S000_"))