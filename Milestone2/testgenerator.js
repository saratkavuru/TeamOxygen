// Core/NPM Modules
const product = require('iter-tools/lib/product');
const fs      = require("fs");
const mock    = require('mock-fs');
const _       = require('lodash');



// Mock file operations
const mockFileLibrary = {
    pathExists: {
        // 'path/fileExists': {  },
        // 'path/nonempty': { 'file': '' },
        emptyDir: 'mock.directory()',
        nonEmptyDir: 'mock.directory({ items: { file: mock.file() } })',
        file: 'mock.file()'
    },
    fileWithContent: {
        pathContent: {
            file1: "new Buffer('abc')",
            someDir: 'mock.directory()'
        }
    }
};


/**
 * Generate test cases based on the global object functionConstraints.
 *
 * @param {String} filepath            Path to write test file.
 * @param {Object} functionConstraints Constraints object as returned by `constraints`.
 */
function generateTestCases(filepath, functionConstraints) {

    // Content string. This will be built up to generate the full text of the test string.
    let content = `var testadmin = require('./routes/admin.js');
    var MongoClient = require('mongodb').MongoClient;
    var url = "mongodb://admin:password@127.0.01:27017/site?authSource=admin";
    var MongoClient = mongo.MongoClient;
    var db = null;
    MongoClient.connect("mongodb://"+process.env.MONGO_USER+":"+process.env.MONGO_PASSWORD+"@"+process.env.MONGO_IP+":27017/site?authSource=admin", function(err, authdb) {
    db = authdb;
    console.log( err || "connected!" );
    });
    var mongo = require('mongodb');
    var Server = mongo.Server,
    Db = mongo.Db,
    ObjectID = mongo.ObjectID;
    var rewire = require('rewire');
    var chai = require('chai');
    var should = chai.should();
    var testcsv = rewire('./routes/csv.js');
    var request = require('request');

    formatJsonAsCSV = testcsv.__get__('formatJsonAsCSV');

    try {
        var items = {
            votes: [{
                        answers: [{
                            kind: "singlechoice",
                            answer: "yes",
                            question: "name please\\n"
                        },
                        {
                            kind: "singlechoicetable",
                            answer: "yes",
                            question: "name please\\n"
                        },
                        {
                            kind: "textarea",
                            answer: "yes",
                            question: "name please\\n"
                        },
                        {
                            kind: "text",
                            answer: "yes",
                            question: "name please\\n"
                        },
                        {
                            kind: "",
                            answer: "yes",
                            question: "name please\\n"
                        },
                        {
                            kind: "singlechoicetable",
                            answer: "no",
                            question: "name please\\n"
                        }
                        ]}]
        };
        formatJsonAsCSV(items);
        var items = {
            votes: [{
                        answers: [{
                            kind: "singlechoice"
                        },
                        {
                            kind: "singlechoicetable",
                            answer: "yes"
                        },
                        {
                            kind: ""
                        },
                        {
                            kind: "singlechoicetable",
                            answer: "no"
                        }
                        ]}]
        };
        formatJsonAsCSV(items);
    } catch (error) { }
    \n`;

    kindValue = ['AMZN', 'SURFACE', 'IPADMINI', 'GITHUB', 'BROWSERSTACK', ''];
    for(i=0;i<6;i++)
    {

        tokenValue = String.fromCharCode(65+i);
        content += `\n  MongoClient.connect(url, function(err, db) {
                if (err) throw err;
                var dbo = db.db('sites');
                var myobj = { _id: "`+i+`", token: "`+ tokenValue +`", status:'open', kind:"`+kindValue[i]+`"};
                dbo.collection('studies').insertOne(myobj, function(err, res) {
                if (err) throw err;
                console.log('1 document inserted');
                });
            });

            setTimeout(function(){
                try {
                    res = {send : function(param){}};
                    req = {"params":{
                        "id":"`+i+`",
                        "token": "`+tokenValue+`"
                        },
                        "body":{
                            "token": "`+tokenValue+`",
                            "kind": "`+kindValue[i]+`",
                            "email": "abc@abc.com"
                            }};
                    testadmin.notifyParticipant(req, res);
                } catch (error) {
                }
                finally{
                    // db.collection('studies').deleteOne({id: "`+i+`"});
                }
            },1000);\n`
    }
    // Iterate over each function in functionConstraints


    for ( let funcName in functionConstraints ) {
            if (funcName == 'api') {
              console.log("In the api generator");
              console.log(functionConstraints[funcName]);
              for (var i = 0; i < functionConstraints[funcName].length; i++){
                api = functionConstraints[funcName][i];
                content += `setTimeout(function(){
                    try {
                        req = {"params":{
                            "id":"5",
                            "token": "F"
                            },
                            "body":{
                                "token": "F"
                                }};
                        res = {send : function(param){}};
                        var options = {
                          url: 'http://127.0.0.1/`+api.url+`',
                          method: '`+ api.type +`',
                          json: req,
                        };
                        request.post(options , function(error, response, body){
                          console.log(response.status);
                        });
                    } catch (error) {
                    }
                     }, 3000);`;
                 }
            }
            else if (funcName){
                content += `setTimeout(function(){
                    try {
                        req = {"params":{
                            "id":"5",
                            "token": "F"
                            },
                            "body":{
                                "token": "F"
                                }};
                        res = {send : function(param){}};
                        testadmin.`+funcName+`(req, res);
                    } catch (error) {
                    }
                     }, 3000);`;
            }
        }

        content += `setTimeout(function(){
            try {
                db.collection('studies').drop();
            } catch (error) {
            }
        }, 4000);`;
    // Write final content string to file test.js.
    fs.writeFileSync('test.js', content, "utf8");

}

// Export
module.exports = generateTestCases;
