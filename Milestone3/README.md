# Milestone 1 - Configuration Management and Build Milestone

## Contribution:

- Anshuman Goel (agoel5) : Installing and configuring Jenkins on a remote server
- Divya Guttikonda (dguttik) : Deploying iTrust on a remote server
- Sarat Kavuru (skavuru) : Node.js script for provisioning an EC2 instance and deploying Checkbox on a remote server
- Tanmay Goel (tgoel) : Create jobs and run builds in Jenkins for Checkbox and iTrust

## Screencast
[Screencast for Demo of  Configuration Management and Build Milestone](https://youtu.be/ZiYr0PUvH7c)

## Report

### Few Notes:

- The ansible-vault file should be named __credys.yml__ and the following credentials should be stored in as key:value pairs (DOTOKEN : 'xxx').
  - AWSAccessKeyId
  - AWSSecretKey
  - git_username
  - git_password
 - AWSAccessKeyId, AWSSecretKey are the accesskeyId and secretKey of an AWS account and git_username, git_password  are the username and password of a Github Ncsu Enterprise account.
- Create an SSH key pair with the name DevOps with your AWS account and store the file in the [Milestone1](../Milestone1) directory. Make sure that this key file has read-write permissions 0400 or 0600.
- All the variables required for [checkbox.io](https://github.com/chrisparnin/checkbox.io) are in the file [checkboxvar.yml](../Milestone1/checkboxvar.yml) and they can be modified as required.
- The Node.js file [aws.js](../Milestone1/aws.js) should always be called with ServerName as an argument.
- The commands to run each playbook are placed as comment at the top of of each playbook.
- The ansible-playbook [node.yml](../Milestone1/node.yml) is used to configure a local vm and then run aws.js to provision a remote server for Jenkins.
- The ansible-playbook [JenkinsConfig.yml](../Milestone1/JenkinsConfig.yml) is used to install and configure Jenkins on a remote server. It uses files [CheckBoxBuild.yml](../Milestone1/CheckBoxBuild.yml) and [iTrustBuild.yml](../Milestone1/iTrustBuild.yml) which are parsed by the ```jenkins-job-builder``` to automate the creation of jobs for Jenkins.
- [Checkbox.yml](../Milestone1/Checkbox.yml) and [iTrust.yml](../Milestone1/itrust.yml) are the ansible-playbooks which are executed in the post-build actions of respective Jenkins jobs to provision and configure a VM for each application.
- The ansible-playbook [milestone1.yml](../Milestone1/CheckBoxBuild.yml) is an outer level playbook which executes node.yml and JenkinsConfig.yml playbook and thus automating the entire Milestone 1 to a single step.

 ### Experience:

 - Since, most of us haven't worked with Jenkins earlier, 
 figuring out what exactly Jenkins is and how to use it for automation of pipeline , setting it up and dealing with the authentication for Jenkins user took a little more time than expected. 

 - Lack of prior experience with ```jenkins-job-builder``` was the reason why we initially felt that automating Jenkins jobs and builds was a very complex and time-consuming task. Having successfully completed the milestone, we realize how automation of a deployment pipeline using Jenkins is incredibly useful, especially for applications in deployment.
 
 - To figure out exactly how ```jenkins-job-builder``` worked, we initially had to do some reverse engineering by building a job through UI and build using a yml file for ```jenkins-job-builder``` and then compare the config.xml generated in both situations.

 - While trying out different ways to run the build, we encountered a [Jenkins bug](https://issues.jenkins-ci.org/browse/JENKINS-43346) which is still open and the documentation was not clear enough for us to figure out how exactly to use jenkins-cli commands using username and password. After some research, we've found a workaround for it using ```build-token-root```.
 
 - While trying to deploy checkbox.io , we've encountered some trouble while trying to set up a mongodb user and accessing the checkbox application. After going through the configuration files and actual code of the appication, we've ended up using mongodb_user ansible module and setting [MONGO_PORT] according to the code in server.js and replacing one of the lines in the config files.

 - Configuring and provisioning [iTrust](https://github.ncsu.edu/engr-csc326-staff/iTrust2-v2) wasn't easy as well since we spent a lot of time setting up Tomcat and copying many configuration files but then realized setting up Tomcat wasn't absolutely necessary.
