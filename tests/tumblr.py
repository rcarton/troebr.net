#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from troebr import tumblr

class TestTumblr(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def test_get_posts(self):
        posts = tumblr.get_posts()
        self.assertGreater(len(posts), 0)


if __name__ == '__main__':
    unittest.main()
    