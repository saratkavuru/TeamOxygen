import fnmatch
import os
import re
import random
import requests
import time
import subprocess
import pymysql

sha1 = ""

def fuzzing():
	files = []
	dir_name = "/var/lib/jenkins/jobs/iTrust/workspace/iTrust2-v1/iTrust2/src/main/java/edu/ncsu/csc/itrust2"
	# print(dir_name)
	for root, dirnames, filenames in os.walk(dir_name):
		for filename in fnmatch.filter(filenames, '*.java'):
			if "models" in root or "mysql" in root or "test" in root or "AddApptRequestAction.java" in filename:
				continue
			files.append(os.path.join(root, filename))

	random.seed()
	prob = random.randint(1,1001)
	random.seed()
	prob2 = random.randint(1,1001)
	if prob2 < 1000:
		for file_name in files:

			f = open(file_name, 'r')
			lines = f.readlines()
			lines1 = lines
			lines2 = []

			for line in lines:
				if((re.match('(.*)if(.*)',line) is not None or re.match('(.*)while(.*)',line) is not None ) and re.match('(.*)<(.*)',line) is not None and re.match('.*<.+>.*',line) is None):
					if(prob < 125):
						print(line)
						line = re.sub('<','>',line)
						print(line)

				if((re.match('(.*)if(.*)',line) is not None or re.match('(.*)while(.*)',line) is not None ) and re.match('(.*)>(.*)',line) is not None):
					if(prob >= 125 and prob < 250):
						print(line)
						line = re.sub('>','<',line)
						print(line)

				if((re.match('(.*)if(.*)',line) is not None or re.match('(.*)while(.*)',line) is not None ) and re.match('(.*)==(.*)',line) is not None):
					if(prob >= 250 and prob < 375):
						print(line)
						line = re.sub('==','!=',line)
						print(line)

				if((re.match('(.*)if(.*)',line) is not None or re.match('(.*)while(.*)',line) is not None ) and re.match('(.*)!=(.*)',line) is not None):
					if(prob >= 375 and prob < 500):
						print(line)
						line = re.sub('!=','==',line)
						print(line)

				if ((re.match('(.*)if(.*)',line) is not None or re.match('(.*)while(.*)',line) is not None ) and re.match('(.*) 0(.*)',line) is not None):
					if(prob >= 500 and prob < 625):
						print(line)
						line = re.sub(' 0',' 1',line)
						print(line)

				if ((re.match('(.*)if(.*)',line) is not None or re.match('(.*)while(.*)',line) is not None ) and re.match('(.*) 1(.*)',line) is not None):
					if(prob >= 625 and prob < 700):
						print(line)
						line = re.sub(' 1',' 0',line)
						print(line)

				if re.findall(r'\"(.+?)\"',line) and 'reject' not in line and 'allActions' not in line and 'ResponseEntity' not in line and 'ROLE' not in line and 'port' not in line and '#' not in line and 'setEmail' not in line and '@' not in line and 'SimpleDateFormat' not in line and 'addAttribute' not in line and 'getProperty' not in line and 'put' not in line and '/' not in line and 'Query' not in line and '?' not in line :
					if(prob >= 700 and prob < 1001):
						print(line)
						match = re.findall(r'\"(.+?)\"',line)
						if(match[0]!=' ' and match[0]!=''):
							line = line.replace(match[0], "not" + match[0])
						print(line)

				lines2.append(line)

			fout = open(file_name,'w')
			for l in lines2:
				fout.write(l)

def gitCommit(i):
	command = 'cd  /var/lib/jenkins/jobs/iTrust/workspace/iTrust2-v1 && git add --all . && git commit -am "fuzzing commit '+str(i)+'"'
	os.system(command)
	sha1 = os.popen('git rev-parse HEAD').read()

def jenkins():
	pas = os.popen('sudo cat /var/lib/jenkins/secrets/initialAdminPassword').read().strip()
	requests.get("http://127.0.0.1:8081/buildByToken/build?job=iTrust&token=8fc61f12b36588bf13393a30a6af61e6")
	response = requests.get('http://127.0.0.1:8081/job/iTrust/api/json',auth=('admin', pas))
	data = response.json()
	buildNumber = data['nextBuildNumber']
	tries = 0
	while True:
		try:
			response = requests.get('http://127.0.0.1:8081/job/iTrust/' + str(buildNumber)  + '/api/json', auth=('admin', pas))
			data = response.json()
			if data['building'] != False:
				time.sleep(10)
				tries = tries + 1
				if tries > 200:
					break
				continue
			break
		except ValueError:
			continue
	return buildNumber

def revertcommit():
	""" revert the fuzzing commit
	Checks out the master branch and deletes the fuzzer branch
	TODO : Maybe there is no commit.
	"""
	command = 'cd /var/lib/jenkins/jobs/iTrust/workspace/iTrust2-v1 && git checkout master && git branch -D fuzzer'
	os.system(command)

testList = []
def testPriortization(buildNumber):
	failTestCount = 0
	with open('/var/lib/jenkins/jobs/iTrust/builds/'+str(buildNumber)+'/log', 'r') as logfile:
		for cnt, line in enumerate(logfile):
			failed = False
			test = re.search(" FAILURE! - in",line)
			if test:
				failTestCount = failTestCount + 1
				failed = True
			test = re.search("Tests run: (\d+), .*- in (.*)\n",line)
			if test:
				testName = line[line.index(" - in ")+6:len(line)-1]
				time = float(line[line.index("Time elapsed: ")+14:line.index(" s")])
				if failed:
					testList.append((testName, time, "Failed"))
				else:
					testList.append((testName, time, "Passed"))
	return failTestCount

def main():
	failTestCount = 0
	for i in range(1):
		command = 'cd /var/lib/jenkins/jobs/iTrust/workspace/iTrust2-v1 && git checkout -B fuzzer'
		os.system(command)
		fuzzing()
		gitCommit(i)
		buildNumber = jenkins()
		revertcommit()
		failTestCount = failTestCount + testPriortization(buildNumber)
	
	with open("/home/ubuntu/iTrust/priortization.dat", 'w+') as f:
		f.write(str(testList))
		# testList.sort(key=lambda x: x[1])
		# print(testList)
		# print("Number of test cases failed ", str(failTestCount))
	
	try:
		connection = pymysql.connect(host="127.0.0.1", user="root", password="", charset="utf8mb4", cursorclass=pymysql.cursors.DictCursor)
		dbCursor = connection.cursor()
		dbCursor.execute("DROP DATABASE itrust2")
	
	except Exception as e:
		print("Exeception occured:{}".format(e))
		
	finally:
		connection.close()

if __name__ == "__main__":
	main()
