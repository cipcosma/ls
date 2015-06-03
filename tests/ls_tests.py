'''
Unittests for the ls module

@license: "GPL"
@author: "Ciprian Cosma"
'''
import unittest
import ls
import os


class ArgsTest(unittest.TestCase):
    '''Tests for the argument parser function'''

    def test_arguments_empty(self):
        '''All empty arguments, expecting the current dir'''
        file_list = []
        file_list.append(os.getcwd())
        self.assertEqual((False, False, False, False, False,
                          False, file_list),
                         ls.parse_arguments([]))

    def test_file_list(self):
        '''Multiple files in a list'''
        file_list = ['a', 'b']
        self.assertEqual((False, False, False, False, False,
                          False, file_list),
                         ls.parse_arguments(['a', 'b']))

    def test_arguments_full(self):
        '''All options set'''
        file_list = ['a', 'b']
        self.assertEqual((True, True, True, True, True,
                          False, file_list),
                         ls.parse_arguments(['-haltR', 'a', 'b']))


if __name__ == "__main__":
    unittest.main()
