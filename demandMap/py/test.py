import os

if __name__ == "__main__":
	test = "122px"
	temp = float(test.replace("px" , '')) / 162 * 100
	#percent = str(temp)
	#print(percent)
	#for i in range(2 , 17):
	#	print(i)
	a = 51.19598765432099
	b = float('%.2f' % temp)
	print(b)
