from TrieNodeAbstract import TrieNodeAbstract
from ChildrenDictionary import ChildrenDictionary
import math
from typing import Dict, List, Union
# For help in traversing children
ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


class TrieTree(TrieNodeAbstract):
    def __init__(self, char='', value: str = ''):
        '''
        Initializes:
            This node's char, `self._char`, ie. your current character in the key
            This node's set of subtrees, 'children', using a dictionary
            This node's value, `self._value`  only set iff its a valid word in the dictionary
        '''
        self._value = value
        self._children: ChildrenDictionary = ChildrenDictionary()
        self._char = char

    # TASK 1
    def insert(self, word: str) -> None:
        '''
        Insert your new word, keep in mind, you must insert all child nodes
        >>> trie = TrieTree()
        >>> trie.insert("word")
        >>> trie.insert("water")
        >>> trie.insert("banana")
        >>> "word" in str(trie)
        True
        >>> "water" in str(trie)
        True
        >>> "bob" in str(trie)
        False
        >>> "banana" in str(trie)
        True
        '''
        obj = self
        for letter in word:
            if letter not in obj._children:
                obj._children.__setitem__(letter, TrieTree(letter))
                prev = obj
                obj = obj._children[letter]
            else:
                prev = obj
                obj = obj._children[letter]
        if obj._children is {}:
            prev._children.__setitem__(letter, TrieTree(letter, word))
        else:
            prev._children[word[-1]]._value = word

    # TASK 2
    def __contains__(self, key: str) -> bool:
        '''
        Returns True iff key is in tree, otherwise False
        >>> trie = TrieTree()
        >>> trie.insert("word")
        >>> "word" in trie
        True
        >>> "other" in trie
        False
        '''
        obj = self
        for letter in key:
            if letter not in obj._children:
                return False
            obj = obj._children[letter]
        if obj._value == key:
            return True
        return False

    # TASK 3
    def __delitem__(self, key: str):
        '''
        Deletes entry in tree and prunes unecessary branches if key exists, otherwise changes nothing
        >>> trie = TrieTree()
        >>> trie.insert("word")
        >>> "word" in trie
        True
        >>> del trie["word"]
        >>> "word" in trie
        False
        >>> str(trie)
        'TrieTree'
        >>> trie.insert('ab')
        >>> trie.insert('abs')
        >>> str(trie)
        'TrieTree\\n   `- a\\n      `- b : ab\\n         `- s : abs'
        >>> del trie['ab']
        >>> str(trie)
        'TrieTree\\n   `- a\\n      `- b\\n         `- s : abs'
        '''
        obj = self
        arg = key[0]
        if key[0] in self._children:
            startdel = self
        for letter in range(len(key) - 1):
            if key[letter] in obj._children:
                if len(obj._children) > 1 or (obj._children[key[letter]]._value != '' and \
                    obj._children[key[letter]]._value != key):
                    startdel = obj._children[key[letter]]
                    arg = key[letter + 1]
                obj = obj._children[key[letter]]
        if obj != self:
            if obj._children[key[-1]]._value == key:
                if obj._children[key[-1]]._children != {}:
                    obj._children[key[-1]]._value = ''
                else:
                    startdel._children.pop(arg)

    # TASK 4
    def sort(self, decreasing=False):
        '''
        Returns list of words in tree sorted alphabetically
        >>> trie = TrieTree()
        >>> trie.insert('banana')
        >>> trie.insert('cherry')
        >>> trie.insert('apple')
        >>> trie.sort()
        ['apple', 'banana', 'cherry']
        >>> trie.sort(decreasing=True)
        ['cherry', 'banana', 'apple']
        '''
        obj = self
        lst = TrieTree.sorthelper(self, obj, [])
        if decreasing:
            return lst[::-1]
        return lst

    def sorthelper(self, level, lst):
        for letter in ALPHABET:
            if letter in level._children:
                if level._children[letter]._value != '':
                    lst.append(level._children[letter]._value)
                if level._children[letter]._children is not {}:
                    TrieTree.sorthelper(self, level._children[letter], lst)
        return lst

    # TASK 5
    def autoComplete(self, prefix, N=10):
        '''
        if given a valid prefix, return a list containing N number of suggestions starting with that prefix in alphabetical order
        else return an empty list
        >>> trie = TrieTree()
        >>> trie.insert('apple')
        >>> trie.insert('dad')
        >>> trie.insert('apples')
        >>> trie.insert('application')
        >>> trie.insert('app')
        >>> trie.insert('about')
        >>> trie.autoComplete('a')
        ['about', 'app', 'apple', 'apples', 'application']
        >>> trie.autoComplete('a', N=2)
        ['about', 'app']
        >>> trie.autoComplete('app')
        ['app', 'apple', 'apples', 'application']
        >>> trie.autoComplete('c')
        []
        >>> trie.autoComplete('d')
        ['dad']
        '''
        obj = self
        for letter in prefix:
            if letter not in obj._children:
                return []
            obj = obj._children[letter]
        autocompletelist = []
        if obj._value != '':
            autocompletelist = [obj._value]
        lst = TrieTree.autocompletehelper(self, obj, autocompletelist, N)
        return lst

    def autocompletehelper(self, level, lst, N):
        for letter in ALPHABET:
            if letter in level._children:
                if level._children[letter]._value != '':
                    lst.append(level._children[letter]._value)
                if len(lst) == N:
                    return lst
                if level._children[letter]._children is not {}:
                    TrieTree.sorthelper(self, level._children[letter], lst)
        return lst

    # TASK 6
    def autoCorrect(self, word, errorMax=2):
        '''
        Given a word, if misspelt return a list of possible valid words from the last valid prefix, with up to errorMax errors
        >>> trie = TrieTree()
        >>> trie.insert('dab')
        >>> trie.autoCorrect('dod')
        ['dab']
        >>> trie.autoCorrect('dod', errorMax=1)
        []
        >>> trie.autoCorrect('dad', errorMax=1)
        ['dab']
        >>> trie.insert('apple')
        >>> trie.insert('dad')
        >>> trie.insert('dude')
        >>> trie.insert('apples')
        >>> trie.insert('application')
        >>> trie.insert('app')
        >>> trie.insert('about')
        >>> trie.insert("apples")
        >>> trie.insert("application")
        >>> trie.insert('app')
        >>> trie.insert('apple')
        >>> trie.autoCorrect('apl', errorMax=10)
        ['app', 'apple', 'apples', 'application']
        >>> trie.autoCorrect('aboot')
        ['about']
        >>> trie.autoCorrect('dea')
        ['dab', 'dad']
        >>> trie.autoCorrect('dod')
        ['dad', 'dude']
        >>> trie.autoCorrect('dea', errorMax=3)
        ['dab', 'dad', 'dude']
        '''
        if TrieTree.__contains__(self, word):
            return [word]
        lst = TrieTree.sort(self)
        lst2 = []
        for item in lst:
            if len(item) < len(word) + errorMax:
                index = None
                numcorrect = 0
                for letter in range(len(word)):
                    if word[letter] in item:
                        if index is None:
                            index = item.index(word[letter])
                            numcorrect += 1
                        else:
                            if index < len(item) - 1:
                                if item[index + 1] == word[letter]:
                                    numcorrect += 1
                            index += 1
                if len(item) - numcorrect <= errorMax:
                    lst2.append(item)
        return lst2

    # TASK 7
    def merge(self, otherTrie: TrieNodeAbstract):
        '''
        Merges another TrieTree into this one
        >>> trie1 = TrieTree()
        >>> trie2 = TrieTree()
        >>> trie1.insert('amazing')
        >>> trie2.insert('amazon')
        >>> trie1.merge(trie2)
        >>> 'amazon' in trie1
        True
        '''
        lst = otherTrie.sort()
        for item in lst:
            TrieTree.insert(self, item)

    def pPrint(self, _prefix="", _last=True, index=0):
        '''
        DONT CHANGE THIS
        '''
        ret = ''
        if index:
            ret = _prefix + ("`- " if _last else "|- ") + self._char
            _prefix += "   " if _last else "|  "
            if self._value:
                ret += ' : ' + self._value
            ret += '\n'
        else:
            ret = _prefix + "TrieTree"
            _prefix += "   " if _last else "|  "
            ret += '\n'
        child_count = len(self._children)
        for i, child in enumerate(self._children):
            _last = i == (child_count - 1)
            ret += self._children[child].pPrint(_prefix, _last, index+1)
        return ret

    def __str__(self):
        return self.pPrint().strip()


if __name__ == '__main__':
    import doctest
    doctest.testmod()
