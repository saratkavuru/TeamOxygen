var AWS = require('aws-sdk');
var fs = require('fs');
var ServerName = process.argv[2];
if (process.argv.length>3)
    var numberOfInstances = process.argv[3];
else
    var numberOfInstances = 1;

AWS.config.update({
    accessKeyId: process.env.AWSAccessKeyId,
    secretAccessKey: process.env.AWSSecretKey,
    region: "us-east-1"
});

var ec2 = new AWS.EC2({apiVersion: '2016-11-15'});

var params = 
{
    ImageId : "ami-a22323d8",
    InstanceType : "t2.micro",
    MinCount : 1,
    MaxCount : 1,
    KeyName: 'DevOps',
    TagSpecifications: [
        {
          ResourceType:  "instance" ,
          Tags: [
            {
              Key: 'Name',
              Value: ServerName
            },
          ]
        },
      ],
    
};

fs.appendFile("inventory","["+ServerName+"]"+ "\n", (err) =>{
    if (err) throw err;
    console.log("Jenkins added to inventory");
});

for(var i=0;i<numberOfInstances;i++)
{
    ec2.runInstances(params, function(err,data){
        if(err){
            console.log("Instance cannot be created", err);
        }
        else{
            // Grab instanceID in this callback.
            // console.log(data);
            var instanceID = data.Instances[0].InstanceId;
            console.log("InstanceID: ", instanceID);
            console.log("Fetching IP");
            
            // Function to grab IP address.
            var params ={
                InstanceIds:[instanceID]
            };
            
            setTimeout(function(){
                ec2.describeInstances(params,function(err, data){
                    if (err){
                        console.log("Instance cannot be described",err);
                    }
                    else{
                        //Grab the IP address in this callback.
                        // console.log(data.Reservations[0].Instances);
                        var ip = data.Reservations[0].Instances[0].PublicIpAddress;
                        var dns = data.Reservations[0].Instances[0].PublicDnsName;
                        console.log("IP Address:", ip);
                        console.log("Public DNS:", dns);
                        fs.appendFile("dns.yml",ServerName+"Dns: "+ dns +"\n" ,(err)=>{
                            if (err) throw err;
                            console.log("DNS added to JSON");
                        });
                        fs.appendFile("inventory", ip + ' ansible_ssh_user=ubuntu ' + 'ansible_ssh_private_key_file=DevOps.pem '+'ansible_ssh_common_args=\'-o StrictHostKeyChecking=no\'\n\n',(err)=>{
                            if (err) throw err;
                                console.log("Jenkins added to inventory");
                        });
                    }
                });
            },15000);
        }
    });
}

