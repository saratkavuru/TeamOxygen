# DevTech

#### Few Notes:

- creds.yml Ansible vault file.
 - The credentials (AWSAccessKeyId, AWSSecretKey, git_username, git_password ) for GitHub and AWS accounts should be stored in an ansible vault file in the Ansible directory as key:value pairs (DOTOKEN : 'xxx').
 - DevOps.pem should be the name of the ssh keyfile to AWS.

 ## Experience:

 Understanding what Jenkins is and what does build mean took lot of time. After that it starts with provisoning and configuring the Jenkins on AWS EC2 instance.

 Jenkins has lot of bugs and not clear documentation of handling the jenkins-cli commands using username and password. Different workaround have to be figured out like ```build-token-root```.

 Lack of knowledge in ```jenkins-job-builder``` also took time. To make it we did some reverse engineering by building a job through UI and build the ```jenkins-job-builder``` yml file through config.xml generated through UI.

 Understanding of iTrust provisoning took time as we spent lot of time on tomcat which wasn't required.
