var AWS = require('aws-sdk');
var fs = require('fs');

AWS.config.update({
    accessKeyId: process.env.AWSAccessKeyId,
    secretAccessKey: process.env.AWSSecretKey,
    region: "us-east-1"
});

var ec2 = new AWS.EC2({apiVersion: '2016-11-15'});


// Grab instanceID in this callback.
// console.log(data);
// var instanceID = data.Instances[0].InstanceId;
// console.log("InstanceID: ", instanceID);
// console.log("Fetching IP");

// Function to grab IP address.
// var params ={
//     InstanceIds:[instanceID]
// };

var params = {
    Filters: [
        {
            Name: 'instance-state-name',
            Values: [
                'running'
            ],
        }, 
        {
            Name: 'tag:Name',
            Values: [
                'master-us-east-1a-1.masters.devtech.k8s.local',
                /* more items */
            ]
        },
        /* more items */
    ],
};

ec2.describeInstances(params,function(err, data){
    if (err){
        console.log("Instance cannot be described",err);
    }
    else{
        //Grab the IP address in this callback.
        instances = [];
        console.log(data);
        for(i=0;i<data.Reservations.length;i++){
            instances.push(data.Reservations[i].Instances[0].InstanceId);
        }
        console.log(instances);

        var params ={
            InstanceIds:[instances[0]]
        };
        
        ec2.terminateInstances(params, function(err, data) {
            if (err) console.log(err, err.stack); // an error occurred
            else     console.log(data);           // successful response
          });
    }
});
