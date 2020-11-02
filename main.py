import sys
import warnings
import random 

from task.task1 import Task1
from task.task2 import Task2
from task.task3 import Task3

if __name__ == "__main__":
	file_name = sys.argv[1]		

	# For ignoring UserWarnings
	warnings.filterwarnings("ignore")
	bucket_name = 'surfboard-transcribe'

	n = random.randint(0,100000)

	t1 = Task1(file_name,bucket_name, n)
	data = t1.execute_all_functions()

	input("Press Enter to Continue...")

	t2 = Task2(data,file_name)
	speaker_set = t2.execute_all_functions()

	input("Press Enter to Continue...")
	
	t3 = Task3(speaker_set,n)
	t3.execute_all_functions()