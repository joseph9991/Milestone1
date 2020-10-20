import glob, os

for i in glob.glob('spk_*.wav'):
	os.remove(i)