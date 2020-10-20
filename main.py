import sys
import warnings

from task.task1 import Task1
from task.task2 import Task2

if __name__ == "__main__":
	file_name = sys.argv[1]		

	# For ignoring UserWarnings
	warnings.filterwarnings("ignore")
	bucket_name = 'surfboard-transcribe'

	t1 = Task1(file_name,bucket_name)
	data = t1.execute_all_functions()

	input("Press Enter to Continue...")

	t2 = Task2(data,file_name)
	t2.execute_all_functions()
	
	