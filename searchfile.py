import glob

token = '8C-9156'
#filePattern = r'D:\learn\test\**\[F]*'
#filePattern = r'G:\稅處大檔\107稅處大檔\FIE\**\NVABS415*'
filePattern = r'G:\稅處大檔\108_S415\**\NVABS415*'

with open('output.txt', 'w', encoding="utf-8") as fout:
	fileNameList = glob.glob(filePattern, recursive=True)
	for fileName in fileNameList:
		with open(fileName, encoding="utf-8", errors='ignore') as f:
			fout.write('*********************************************\n')
			fout.write(fileName + '\n')
			for line in f:
				if token in line:
					fout.write(line)
	