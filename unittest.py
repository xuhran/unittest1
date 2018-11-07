import unittest
import HTMLTestRunner
from baidu import baidusearch
class mytest(unittest.TestCase):
    def tearDown(self):
        print('111')
    def setUp(self):
        print('222')
    @classmethod
    def tearDownClass(self):
        print('444')
    @classmethod
    def setUpClass(self):
        print('333')
    def test_a_run(self):
        self.assertIsNotNone('dhjsk')
    def test_b_run(self):
        self.assertIsNotNone('123456')
    def test_c_run(self):
        self.assertIsNotNone('鬼哥鬼哥我爱你')
    def test_d_run(self):
        self.assertIsNotNone('kobe`')
if __name__ == '__main__':
    test_suit = unittest.test_suit()
    test_suit.addTest(unittest.makesuite(mytest))
    fp = open('test.html','wb')
    runner = HTMLTestRunner.HTMLTestRunner(stream=fp,title='test report',description='test details')
    runner.run(test_suit)