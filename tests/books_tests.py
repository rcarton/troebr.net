#!/usr/bin/env python
# -*- coding: utf-8 -*-
import unittest
from troebr import books

class TestBooks(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_get_books(self):
        items = books.get_items()
        self.assertGreater(len(items), 0)
        
if __name__ == '__main__':
    unittest.main()
    