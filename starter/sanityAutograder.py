import json
import os
CREATE_TESTS = False


# COMMENT OUT ANY NOT YET IMPLEMENTED THINGS TO SEE IF YOUR CODE WORKS

def loadDictionary(amount=100, seed='69420'):
    from TrieTree import TrieTree
    import random
    random.seed(seed)
    trie = TrieTree()
    with open('dictionary', 'r') as words:
        wordLst = words.readlines()
        try:
            for i in range(random.randint(0, int(len(wordLst)/amount)), len(wordLst), int(len(wordLst)/amount)):
                trie.insert(wordLst[i].strip())
        except TimeoutError:
            return None
    return trie


def insertTests():
    currMark = 0
    totalMarks = 0
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nRunning Insert Tests...\n')
    for filename in os.listdir('sanityTests/insert/'):
        totalMarks += 1
        with open('sanityTests/insert/{}'.format(filename)) as f:
            testData = json.load(f)
            outStr = '{}\t TEMP\n'.format(testData['name'])
            testTrie = loadDictionary(
                testData['amount'], testData['seed'])
            if not testTrie:
                outStr += 'Exception during testing above\n'
                outStr = outStr.replace('TEMP', '0/1')
                print(outStr)
            elif (str(testTrie).replace(' ', '') != testData['expectedTreeString'].replace(' ', '')):
                if CREATE_TESTS:
                    print(str(testTrie).replace('\n', '\\n').replace(' ', ''))
                else:
                    outStr += 'Expected:\n{}\nReceived:\n{}'.format(
                        testData['expectedTreeString'], str(testTrie))
                    outStr = outStr.replace('TEMP', '0/1')
            else:
                currMark += 1
                outStr = outStr.replace('TEMP', '1/1', 1)
            print(outStr)
    print('Insert Tests total : {}/{}\n'.format(currMark, totalMarks))
    return (currMark, totalMarks)


def containsTests():
    currMark = 0
    totalMarks = 0
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nRunning Contains Tests...\n')
    for filename in os.listdir('sanityTests/contains/'):
        totalMarks += 1
        with open('sanityTests/contains/{}'.format(filename)) as f:
            testData = json.load(f)
            outStr = '{}\t TEMP\n'.format(testData['name'])
            testTrie = loadDictionary(
                testData['amount'], testData['seed'])
            try:
                for word in testData['insert']:
                    testTrie.insert(word)
            except Exception:
                testTrie = None
            if not testTrie:
                outStr += 'Exception during testing above\n'
                outStr = outStr.replace('TEMP', '0/1')
                print(outStr)
            else:
                succ = True
                for word in testData['testWords']:
                    succ = succ and word in testTrie
                if succ != testData['expectedBoolean']:
                    outStr += 'Expected:\n{}\nReceived:\n{}'.format(
                        testData['expectedTreeString'], str(testTrie))
                    outStr = outStr.replace('TEMP', '0/1')
                else:
                    currMark += 1
                    outStr = outStr.replace('TEMP', '1/1', 1)
                print(outStr)
    print('Contains Tests total : {}/{}\n'.format(currMark, totalMarks))
    return (currMark, totalMarks)


def deleteTests():
    currMark = 0
    totalMarks = 0
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nRunning Delete Tests...\n')
    for filename in os.listdir('sanityTests/delete/'):
        totalMarks += 1
        with open('sanityTests/delete/{}'.format(filename)) as f:
            testData = json.load(f)
            outStr = '{}\t TEMP\n'.format(testData['name'])
            testTrie = loadDictionary(
                testData['amount'], testData['seed'])
            try:
                for word in testData["delete"]:
                    del testTrie[word]
            except Exception:
                testTrie = None
            if not testTrie:
                outStr += 'Exception during testing above\n'
                outStr = outStr.replace('TEMP', '0/1')
                print(outStr)
            else:
                succ = True
                for word in testData["delete"]:
                    succ = succ and word not in testTrie
                succ2 = True
                if (str(testTrie).replace(' ', '') != testData['expectedTreeString'].replace(' ', '')):
                    succ2 = False
                    if CREATE_TESTS:
                        print(str(testTrie).replace(
                            '\n', '\\n').replace(' ', ''))
                    else:
                        outStr += 'Expected:\n{}\nReceived:\n{}'.format(
                            testData['expectedTreeString'], str(testTrie))
                currMark += (int(succ) + int(succ2))/2
                outStr = outStr.replace(
                    'TEMP', '{}/1'.format((int(succ) + int(succ2))/2), 1)
            print(outStr)
    print('Delete Tests total : {}/{}\n'.format(currMark, totalMarks))
    return (currMark, totalMarks)


def sortTests():
    currMark = 0
    totalMarks = 0
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nRunning Sort Tests...\n')
    for filename in os.listdir('tests/sort/'):
        totalMarks += 1
        with open('tests/sort/{}'.format(filename)) as f:
            testData = json.load(f)
            outStr = '{}\t TEMP\n'.format(testData['name'])
            testTrie = loadDictionary(
                testData['amount'], testData['seed'])
            sol = None
            try:
                sol = testTrie.sort(testData['reverse'])
            except Exception:
                sol = None
            if not testTrie or not sol:
                outStr += 'Exception during testing above\n'
                outStr = outStr.replace('TEMP', '0/1')
                print(outStr)
            else:
                if sol != testData['expectedOrder']:
                    outStr += 'Expected:\n{}\nReceived:\n{}'.format(
                        testData['expectedOrder'], sol)
                    outStr = outStr.replace('TEMP', '0/1')
                else:
                    currMark += 1
                    outStr = outStr.replace('TEMP', '1/1', 1)
                print(outStr)

    print('Contains Tests total : {}/{}\n'.format(currMark, totalMarks))
    return (currMark, totalMarks)


def autoCompleteTests():
    currMark = 0
    totalMarks = 0
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\nRunning Auto-Complete Tests...\n')
    for filename in os.listdir('tests/autoComplete/'):
        totalMarks += 1
        with open('tests/autoComplete/{}'.format(filename)) as f:
            testData = json.load(f)
            outStr = '{}\t TEMP\n'.format(testData['name'])
            testTrie = loadDictionary(
                testData['amount'], testData['seed'])
            sol = None
            try:
                for word in testData['insert']:
                    testTrie.insert(word)
                sol = testTrie.autoComplete(
                    testData['prefix'], testData['N'])
            except Exception:
                testTrie = None
                sol = None
            if not testTrie or not sol:
                outStr += 'Exception during testing above\n'
                outStr = outStr.replace('TEMP', '0/1')
                print(outStr)
            else:
                if sol != testData['expectedSuggestions']:
                    outStr += 'Expected:\n{}\nReceived:\n{}'.format(
                        testData['expectedSuggestions'], sol)
                    outStr = outStr.replace('TEMP', '0/1')

                else:
                    currMark += 1
                    outStr = outStr.replace('TEMP', '1/1', 1)
                print(outStr)
    print('Auto-Complete Tests total : {}/{}\n'.format(currMark, totalMarks))
    return (currMark, totalMarks)


if __name__ == '__main__':
    testFns = [insertTests, containsTests,
               deleteTests, sortTests, autoCompleteTests]
    totalMarks = 0
    currMarks = 0
    for test in testFns:
        succ, num = test()
        totalMarks += num
        currMarks += succ
    print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n')
    print('Total Mark: [{}/{}]\n'.format(currMarks, totalMarks))
