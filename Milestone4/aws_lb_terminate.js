var AWS = require('aws-sdk');
AWS.config.update({
    accessKeyId: process.env.AWSAccessKeyId,
    secretAccessKey: process.env.AWSSecretKey,
    region: "us-east-1"
});
var elb = new AWS.ELB();
elb.describeLoadBalancers(params={}, function (err, data) {
  if (err) console.log(err, err.stack); // an error occurred
  else   // successful response
  {
    for(i=0;i<data.LoadBalancerDescriptions.length;i++){      
        if(!data.LoadBalancerDescriptions[i].LoadBalancerName.includes('devtech'))
        {
            console.log(data.LoadBalancerDescriptions[i].LoadBalancerName);
            var params = {
                LoadBalancerName: data.LoadBalancerDescriptions[i].LoadBalancerName
            };
            elb.deleteLoadBalancer(params, function (err, data){
                if (err) console.log(err, err.stack); 
                else console.log(data);
            });
        }
    }
  }          
});