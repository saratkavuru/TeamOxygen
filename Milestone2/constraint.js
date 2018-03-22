// Core/NPM Modules
const esprima = require("esprima");
const faker   = require("faker");
const fs      = require('fs');
const Random  = require('random-js');
const _       = require('lodash');
const randexp = require('randexp');



// Set options
faker.locale  = "en";
const options = { tokens: true, tolerant: true, loc: true, range: true };



// Create random generator engine
const engine = Random.engines.mt19937().autoSeed();


/**
 * Constraint class. Represents constraints on function call parameters.
 *
 * @property {String}                                                          ident      Identity of the parameter mapped to the constraint.
 * @property {String}                                                          expression Full expression string for a constraint.
 * @property {String}                                                          operator   Operator used in constraint.
 * @property {String|Number}                                                   value      Main constraint value.
 * @property {String|Number}                                                   altvalue   Constraint alternative value.
 * @property {String}                                                          funcName   Name of the function being constrained.
 * @property {'fileWithContent'|'fileExists'|'integer'|'string'|'phoneNumber'} kind       Type of the constraint.
 */
class Constraint {
    constructor(properties){
        this.ident = properties.ident;
        this.expression = properties.expression;
        this.operator = properties.operator;
        this.value = properties.value;
        this.altvalue = properties.altvalue;
        this.funcName = properties.funcName;
        this.kind = properties.kind;
    }
}


/**
 * Generate function parameter constraints for an input file
 * and save them to the global functionConstraints object.
 *
 * @param   {String} filePath Path of the file to generate tests for.
 * @returns {Object}          Function constraints object.
 */
function constraints(filePath) {

    // Initialize function constraints directory
    let functionConstraints = {};

    // Read input file and parse it with esprima.
    let buf = fs.readFileSync(filePath, "utf8");
    let result = esprima.parse(buf, options);

    // Start traversing the root node
    traverse(result, function (node) {

        if (node.type === 'CallExpression' && node.callee.object && node.callee.object.name == 'app' && node.arguments[0].type == 'Literal' && node.arguments[0].value.startsWith('/api')){
          // console.log(node.arguments);
          if (!('api' in functionConstraints)) functionConstraints['api'] = [];
          let expression = buf.substring(node.arguments[node.arguments.length - 1].range[0], node.arguments[node.arguments.length - 1].range[1]);
          // console.log(expression);
          functionConstraints['api'].push({
            url: node.arguments[0].value,
            method: expression,
            type: node.callee.property.name,
            file: expression.split('.')[0]+'.js',
          });
          // console.log(expression.split('.')[0]+".js");
          // var a = constraints('../checkbox.io/server-side/site/routes/' + expression.split('.')[0]+".js")
          // console.log(a);
          // return;
        }

        // If some node is a function declaration, parse it for potential constraints.
        if (node.type === 'ExpressionStatement' && node.expression.type === 'AssignmentExpression'
            && node.expression.left && node.expression.left.property) {

            //console.log(node.expression.left.property.name);
            // Get function name and arguments
            let funcName = node.expression.left.property.name;//functionName(node);
            //let params = node.params.map(function(p) {return p.name});
            let objectParams = []

            // Initialize function constraints
            functionConstraints[funcName] = {
                //constraints: _.zipObject(params, _.map(params, () => [])),
                //params: params
            };

            //console.log(funcName);
            // Traverse function node.
            traverse(node, function(child) {

                // Handle equivalence expression
                if(_.get(child, 'type') === 'MemberExpression' ){
                    // console.log("here");
                    if (child.object && child.object.type ){
                      // console.log(child.object);
                    }
                }

            });

            // console.log( functionConstraints[funcName]);

        }
    });

    return functionConstraints;
}

/**
 * Traverse an object tree, calling the visitor at each
 * visited node.
 *
 * @param {Object}   object  Esprima node object.
 * @param {Function} visitor Visitor called at each node.
 */
function traverse(object, visitor) {

    // Call the visitor on the object
    visitor(object);

    // Traverse all children of object
    for (let key in object) {
        if (object.hasOwnProperty(key)) {
            let child = object[key];
            if (typeof child === 'object' && child !== null) {
                traverse(child, visitor);
            }
        }
    }
}


/**
 * Return the name of a function node.
 */
function functionName(node) {
    return node.id ? node.id.name : '';
}


/**
 * Generates an integer value based on some constraint.
 *
 * @param   {Number}  constraintValue Constraint integer.
 * @param   {Boolean} greaterThan     Whether or not the concrete integer is greater than the constraint.
 * @returns {Number}                  Integer satisfying constraints.
 */
function createConcreteIntegerValue(constraintValue, greaterThan) {
    if( greaterThan ) return Random.integer(constraintValue + 1, constraintValue + 10)(engine);
    else return Random.integer(constraintValue - 10, constraintValue - 1)(engine);
}


// Export
module.exports = constraints;
