import tscribe
import sys
import time
import datetime

file_name = sys.argv[1]
tscribe.write(file_name,format="csv", save_as="1.csv")
