import fnmatch
import os
import re
import random
import requests
import time
import subprocess
# from useless_iteration import useless

passing = []

#from git import Repo

sha1 = ""

def fuzzing():
	files = []
	dir_name = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
	for root, dirnames, filenames in os.walk(dir_name):
		for filename in fnmatch.filter(filenames, '*.java'):
			if "model" in root or "mysql" in root or "test" in root or "AddApptRequestAction.java" in filename:
				continue
			files.append(os.path.join(root, filename))
	for file_name in files:

		f = open(file_name, 'r')
		lines = f.readlines()
		lt = random.randint(1,1001)
		lines1 = lines
		lines2 = []
		for line in lines:
				
			if(re.match('(.*)if(.*)',line) is not None or re.match('(.*)while(.*)',line) is not None):
				if(re.match('(.*)<(.*)',line) is not None ):
					if(lt < 125):
						line = re.sub('<','>',line)
						# print(line)

			if(re.match('(.*)if(.*)',line) is not None or re.match('(.*)while(.*)',line) is not None):
				if(re.match('(.*)>(.*)',line) is not None):
					if(lt >= 125 and lt < 250):
						line = re.sub('>','<',line)
						# print(line)

			if(re.match('(.*)if(.*)',line) is not None or re.match('(.*)while(.*)',line) is not None):
				if(re.match('(.*)==(.*)',line) is not None):
					if(lt >= 250 and lt < 375):
						line = re.sub('==','!=',line)
						# print(line)

			if(re.match('(.*)if(.*)',line) is not None or re.match('(.*)while(.*)',line) is not None):
				if(re.match('(.*)!=(.*)',line) is not None):
					if(lt >= 375 and lt < 500):
						line = re.sub('!=','==',line)
						# print(line)

			if(re.match('(.*) 0(.*)',line) is not None) and (re.match('(.*)if(.*)',line) is not None or re.match('(.*)while(.*)',line) is not None):
				if(lt >= 500 and lt < 625):
					line = re.sub(' 0',' 1',line)
					# print(line)
	
			if(re.match('(.*) 1(.*)',line) is not None) and (re.match('(.*)if(.*)',line) is not None or re.match('(.*)while(.*)',line) is not None):
				if(lt >= 625 and lt < 700):
					line = re.sub(' 1',' 0',line)
					# print(line)
 	                        
			if(re.match('.*\"(.*)\".*',line) is not None) and (re.match('\".*\\.*\"',line) is not None) and (re.match('\".*@.*\"',line) is not None):
				# print line,"\n"
				if(lt >= 700 and lt <= 1001):
					match = re.search(".*(\".*\").*",line)
					line = line.replace(match.group(1),"\"ThisISRanDOm\"")
					print(line)

			lines2.append(line)

		#os.system('chmod 777 ' + file_name)
		fout = open(file_name,'w')
		for l in lines2:
			fout.write(l)
		# print(file_name)
		
def gitCommit(i):
	dir_name = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
	command = 'cd '+dir_name+'/iTrust2-v2 && git add --all . && git commit -am "fuzzing commit '+str(i)+'"'
	os.system(command)
	sha1 = os.popen('git rev-parse HEAD').read()
	print(sha1)

# def revertcommit(sha):
	
# 	pass = os.popen('cat /var/lib/jenkins/secrets/initialAdminPassword').read().strip()
#         response = requests.get('http://127.0.0.1:8080/job/itrust_job2/api/json',
#                                  auth=('admin', pass))
#         data = response.json()
#         buildNumber = data['nextBuildNumber']
# 	#time.sleep(5)
# 	while True:
# 		#print 'http://159.203.180.176:8080/job/itrust_job2/' + str(buildNumber)  + '/api/json'                
# 		try:
# 			response = requests.get('http://127.0.0.1:8080/job/itrust_job2/' + str(buildNumber)  + '/api/json',
# 								auth=('admin', pass))
# 			data = response.json()
			
# 			if data['building'] != False:
# 				#time.sleep(5)
# 				continue
# 			os.system('git checkout master && git branch -D fuzzer')
# 			break

# 		except ValueError:
# 			#print data
# 			continue
# 	return buildNumber

#	print "-----------------------------------"
#	print data
def main():
	for i in range(2):
		builds = []
		dir_name = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
		command = 'cd '+dir_name+'/iTrust2-v2 && git checkout -B fuzzer'
		os.system(command)
		fuzzing()
		gitCommit(i)
		# builds.append(revertcommit(sha1))
		# val = useless(builds)
		# passing.append(val)
		# print passing
	#print builds

if __name__ == "__main__":
	main()

