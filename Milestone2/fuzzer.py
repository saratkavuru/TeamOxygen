import fnmatch
import os
import re
import random
import requests
import time
import subprocess
import pdb
# from useless_iteration import useless

passing = []

#from git import Repo

sha1 = ""

def fuzzing():
	files = []
	dir_name = "/home/ubuntu"
	print dir_name
	pdb.set_trace()
	for root, dirnames, filenames in os.walk(dir_name):
		for filename in fnmatch.filter(filenames, '*.java'):
			if "model" in root or "mysql" in root or "test" in root or "AddApptRequestAction.java" in filename:
				continue
			files.append(os.path.join(root, filename))
	for file_name in files:

		f = open(file_name, 'r')
		lines = f.readlines()
		lines1 = lines
		lines2 = []
		prob = random.randint(1,1001)

		for line in lines:
			if(re.match('(.*)<(.*)',line) is not None ):
					if(prob < 125):
						line = re.sub('<','>',line)
						# print(line)

			if(re.match('(.*)>(.*)',line) is not None):
					if(prob >= 125 and prob < 250):
						line = re.sub('>','<',line)
						# print(line)

			if(re.match('(.*)==(.*)',line) is not None):
					if(prob >= 250 and prob < 375):
						line = re.sub('==','!=',line)
						# print(line)

			if(re.match('(.*)!=(.*)',line) is not None):
					if(prob >= 375 and prob < 500):
						line = re.sub('!=','==',line)
						# print(line)

			if re.match('(.*) 0(.*)',line) is not None:
				if(prob >= 500 and prob < 625):
					line = re.sub(' 0',' 1',line)
					# print(line)

			if re.match('(.*) 1(.*)',line) is not None:
				if(prob >= 625 and prob < 700):
					line = re.sub(' 1',' 0',line)
					# print(line)

			if re.findall(r'\"(.+?)\"',line) and not line.strip().startswith('@'):
				# print line,"\n"
				if(prob >= 700 and prob <= 1001):
					# print " MATCHED STRING"
					match = matches=re.findall(r'\"(.+?)\"',line)
					line = line.replace(match[0], "NEQ - " + match[0])
					print(line)

			lines2.append(line)

		#os.system('chmod 777 ' + file_name)
		fout = open(file_name,'w')
		for l in lines2:
			fout.write(l)
		# print(file_name)

def gitCommit(i):
	# dir_name = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
	command = 'cd  /home/ubuntu/iTrust2-v2 && git add --all . && git commit -am "fuzzing commit '+str(i)+'"'
	os.system(command)
	sha1 = os.popen('git rev-parse HEAD').read()
	print(sha1)

def jenkins():
	pas = os.popen('cat /var/lib/jenkins/secrets/initialAdminPassword').read().strip()
	response = requests.get('http://127.0.0.1:8080/job/iTrust/api/json',auth=('admin', pas))
	data = response.json()
	buildNumber = data['nextBuildNumber']
	#time.sleep(5)
	while True:
		#print 'http://159.203.180.176:8080/job/itrust_job2/' + str(buildNumber)  + '/api/json'
		try:
			response = requests.get('http://127.0.0.1:8080/job/iTrust/' + str(buildNumber)  + '/api/json', auth=('admin', pas))
			data = response.json()
			if data['building'] != False:
				time.sleep(5)
				continue
			break
		except ValueError:
			#print data
			continue
	print "-----------------------------------"
	print data
	return buildNumber


def revertcommit():
	""" revert the fuzzing commit
	Checks out the master branch and deletes the fuzzer branch
	TODO : Maybe there is no commit.
	"""
	# dir_name = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
	command = 'cd /home/ubuntu/iTrust2-v2 && git checkout master && git branch -D fuzzer'
	os.system(command)

def main():
	for i in range(2):
		builds = []
		# dir_name = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
		command = 'cd /home/ubuntu/iTrust2-v2 && git checkout -B fuzzer'
		os.system(command)
		fuzzing()
		gitCommit(i)
		jenkins()
		revertcommit()
		# builds.append(revertcommit(sha1))
		# val = (builds)
		# passing.append(val)
		# print passing
	#print builds

if __name__ == "__main__":
	main()
