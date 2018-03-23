# [Milestone 2 - Test and Analysis Milestone](https://github.com/CSC-DevOps/Course/blob/master/Project/BuildTestAnalysis.md)

## Contribution:

- Anshuman Goel (agoel5) : Automated commit generation using a commit fuzzer and test prioritization for iTrust.
- Divya Guttikonda (dguttik) : Anisble playbooks for configuring remote server and test generation for checkbox.
- Sarat Kavuru (skavuru) : Coverage report generation using Jacoco jenkins plugin for iTrust and ansible playbooks.
- Tanmay Goel (tgoel) : Test generation using istanbul-middleware for Checkbox.

## Screencast
[Screencast for Demo of  Test and Analysis Milestone](https://www.youtube.com/watch?v=qAbsgiIpf8k)

## Report

### Few Notes:

- The ansible-vault file should be named __credys.yml__ and the following credentials should be stored in as key:value pairs (DOTOKEN : 'xxx').
  - AWSAccessKeyId
  - AWSSecretKey
  - git_username
  - git_password
 - AWSAccessKeyId, AWSSecretKey are the accesskeyId and secretKey of an AWS account and git_username, git_password  are the username and password of a Github Ncsu Enterprise account.
- Create an SSH key pair with the name DevOps with your AWS account and store the file in the [Milestone2](../Milestone2) directory. Make sure that this key file has read-write permissions 0400 or 0600.
- All the variables required for [checkbox.io](https://github.com/goeltanmay/checkbox.io) are in the file [checkboxvar.yml](../Milestone2/checkboxvar.yml) and they can be modified as required.
- The Node.js file [aws.js](../Milestone2/aws.js) should always be called with ServerName as an argument.
- The commands to run each playbook are placed as comment at the top of of each playbook.
- The ansible-playbook [node.yml](../Milestone2/node.yml) is used to configure a local vm and then run aws.js to provision a remote server for Jenkins.
- The ansible-playbook [BuildAndTestAnalysis.yml](../Milestone2/BuildAndTestAnalysis.yml) is used to install all the dependencies, setup Jenkins and generate coverage reports for Checkbox and iTrust on a remote server.
- [main.js](../Milestone2/main.js) , [constraint.js](../Milestone2/constraint.js) and [format-polyfill.js](../Milestone2/format-polyfill.js) are files used in automated test generation for checkbox.io application.
- [fuzzer.py](../Milestone2/fuzzer.py) and [test_prioritization.py](../Milestone2/test_prioritization.py) are the python scripts are used for automated commit generation using a commit fuzzer and test prioritazation of the tests respectively.
- [iTrustBuild.yml](../Milestone2/iTrustBuild.yml) is the yml file which is parsed by the jenkins job builder to create an iTrust job on Jenkins server.
- The ansible-playbook [milestone2.yml](../Milestone2/milestone2.yml) is an outer level playbook which executes node.yml and BuildAndTestAnalysis.yml playbook and thus automating the entire Milestone 2 to a single step.

 ### Experience:
