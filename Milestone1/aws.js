var AWS = require('aws-sdk');

AWS.config.update({
    accessKeyId: process.env.AWSAccessKeyId,
    secretAccessKey: process.env.AWSSecretKey,
    region: "us-east-1"
});

var ec2 = new AWS.EC2({apiVersion: '2016-11-15'});

var params = 
{
    ImageId : "ami-66506c1c",
    InstanceType : "t2.micro",
    MinCount : 1,
    MaxCount : 1,
    KeyName: 'DevOps',
    
};

ec2.runInstances(params, function(err,data){
    if(err){
        console.log("Instance cannot be created", err);
    }
    else{
        // Grab instanceID in this callback.
        console.log(data);
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
                    console.log(data.Reservations[0].Instances);
                    var ip = data.Reservations[0].Instances[0].PublicIpAddress;
                    console.log("IP Address:", ip);
                }
            });
        },15000);
    }
});

