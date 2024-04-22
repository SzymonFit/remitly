import unittest
import json
import re
import os
import sys

class Tests(unittest.TestCase):

    index = 0

    @classmethod
    def setUpClass(cls):
        print('\nStarting test cases...\n')
        
        cls.index = Tests.index
        cls.testData = testData
        cls.testFiles = testFiles

    def testPolicyNameKey(self):
        self.assertIn('PolicyName', self.testData[self.index], 'PolicyName key not found')

    def testPolicyNameLength(self):
        self.assertLessEqual(len(self.testData[self.index]['PolicyName']), 128, 'PolicyName value is too long')

    def testPolicyNameValueType(self):
        self.assertIsInstance(self.testData[self.index]['PolicyName'], str, 'PolicyName value is not of type string')
    
    def testPolicyNameEmpty(self):
        self.assertNotEqual(self.testData[self.index]['PolicyName'], '', 'PolicyName value is empty')

    def testPolicyNameRegex(self):
        self.assertTrue(re.match(r'[\w+=,.@-]+', self.testData[self.index]['PolicyName']), 'PolicyName value contains invalid characters')

    def testPolicyDocumentKey(self):
        self.assertIn('PolicyDocument', self.testData[self.index], 'PolicyDocument key not found')

    def testPolicyDocumentValueType(self):
        self.assertIsInstance(self.testData[self.index]['PolicyDocument'], dict, 'PolicyDocument value is not of type dictionary')
    
    def testPolicyDocumentValue(self):
        self.assertNotEqual(self.testData[self.index]['PolicyDocument'], {}, 'PolicyDocument value is empty')

    def testPolicyDocumentVersion(self):
        self.assertIn('Version', self.testData[self.index]['PolicyDocument'], 'Version key not found in PolicyDocument')

    def testPolicyDocumentVersionValueType(self):
        self.assertIsInstance(self.testData[self.index]['PolicyDocument']['Version'], str, 'Version value is not of type string')

    def testPolicyDocumentStatement(self):
        self.assertIn('Statement', self.testData[self.index]['PolicyDocument'], 'Statement key not found in PolicyDocument')

    def testPolicyDocumentStatementValueType(self):
        self.assertIsInstance(self.testData[self.index]['PolicyDocument']['Statement'], list, 'Statement value is not of type list')

    def testPolicyDocumentStatementEmpty(self):
        self.assertNotEqual(self.testData[self.index]['PolicyDocument']['Statement'], [], 'Statement value is empty')

    def testPolicyDocumentSid(self):
        for stmt in self.testData[self.index]['PolicyDocument']['Statement']:
            self.assertIn('Sid', stmt, 'Sid key not found in Statement')

    def testPolicyDocumentSidValueType(self):
        for stmt in self.testData[self.index]['PolicyDocument']['Statement']:
            self.assertIsInstance(stmt['Sid'], str, 'Sid value is not of type string')
    
    def testPolicyDocumentEffect(self):
        for stmt in self.testData[self.index]['PolicyDocument']['Statement']:
            self.assertIn('Effect', stmt, 'Effect key not found in Statement')

    def testPolicyDocumentEffectValueType(self):
        for stmt in self.testData[self.index]['PolicyDocument']['Statement']:
            self.assertIsInstance(stmt['Effect'], str, 'Effect value is not of type string')

    def testPolicyDocumentEffectValue(self):
        for stmt in self.testData[self.index]['PolicyDocument']['Statement']:
            self.assertIn(stmt['Effect'], ['Allow', 'Deny'], 'Effect value is not valid')

    def testPolicyDocumentAction(self):
        for stmt in self.testData[self.index]['PolicyDocument']['Statement']:
            self.assertIn('Action', stmt, 'Action key not found in Statement')

    def testPolicyDocumentActionValueType(self):
        for stmt in self.testData[self.index]['PolicyDocument']['Statement']:
            self.assertIsInstance(stmt['Action'], list, 'Action value is not of type list')

    def testPolicyDocumentNotEmpty(self):
        self.assertNotEqual(len(self.testData[self.index]['PolicyDocument']), 0, 'PolicyDocument is empty')

    def testPolicyDocumentActionEmpty(self):
        for stmt in self.testData[self.index]['PolicyDocument']['Statement']:
            self.assertNotEqual(stmt['Action'], [], 'Action value is empty')

    def testPolicyDocumentResource(self):
        for stmt in self.testData[self.index]['PolicyDocument']['Statement']:
            self.assertIn('Resource', stmt, 'Resource key not found in Statement')

    def testPolicyDocumentResourceValueType(self):
        for stmt in self.testData[self.index]['PolicyDocument']['Statement']:
            self.assertIsInstance(stmt['Resource'], (str, list), 'Resource value is not of type list')

    def testPolicyDocumentResourceEmpty(self):
        for stmt in self.testData[self.index]['PolicyDocument']['Statement']:
            self.assertNotEqual(stmt['Resource'], '', 'Resource value is empty')
    
    def testPolicyDocumentResourceStars(self):
        for stmt in self.testData[self.index]['PolicyDocument']['Statement']:
            self.assertEqual(stmt['Resource'], '*', "Resource value is '*'")


    @classmethod
    def summary(cls):
        print('\nTest cases completed.\n')
        
        Tests.index += 1

if __name__ == '__main__':
    pathToTestCases = './test/test_cases/'
    validJsonFile = []
    testData = []
    testFiles = [f for f in os.listdir(pathToTestCases) if f.endswith('.json')]

    try:
        if len(testFiles) == 0:
            raise FileNotFoundError('No test cases found in the test_cases directory')
    except FileNotFoundError as e:
        print(f'Error: {e}')
        exit()

    for i, testFile in enumerate(testFiles):
        filePath = os.path.join(pathToTestCases, testFile)
        print(filePath)
        with open(filePath, 'r') as f:
            fileSize = os.stat(filePath).st_size
            if fileSize == 0:
                print(f'{testFile} is empty, file will be ignored.')
                continue
            data = json.load(f)
            testData.append(data)  # Append the contents of the current file

        print(f'Test case:  {i+1}...\nTested file: {testFile}\n')
        result = unittest.TextTestRunner().run(unittest.TestLoader().loadTestsFromTestCase(Tests))
        if result.wasSuccessful():
            validJsonFile.append(testFile)

        testData.clear()
        
    print(testFile)
    print(f'\n\n{"-"*20}\nValid test cases: {validJsonFile}\n{"-"*20}\n\n')