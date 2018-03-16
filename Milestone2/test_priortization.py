import os, ast

with open("/home/ubuntu/iTrust/priortization.dat", 'r') as f:
    testList = ast.literal_eval(f.read())
    testList.sort(key=lambda x: x[1])

failTestCount = 0
for test in testList:
    if test[2] == "Failed":
        failTestCount = failTestCount + 1
    print(test)

print("Number of test cases failed ", str(failTestCount))    