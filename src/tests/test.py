import unittest, sys, os
current_dir = os.path.dirname(os.path.abspath(__file__))
top_level_dir = os.path.abspath(os.path.join(current_dir, '..'))
sys.path.insert(0, top_level_dir)

import ssm_interpreter

class TestSSMFiles(unittest.TestCase):
  
    def test_1(self):
      self.assertEqual(30, ssm_interpreter.compiler("test1.txt"))
    def test_2(self):
      self.assertEqual(60, ssm_interpreter.compiler("test2.txt"))
    def test_3(self):
      self.assertEqual(60, ssm_interpreter.compiler("test3.txt"))
    def test_4(self):
      self.assertEqual(25, ssm_interpreter.compiler("test4.txt"))
      
    def test_5(self):
      self.assertEqual(ValueError, ssm_interpreter.compiler("test5.txt"))
    def test_6(self):
      self.assertEqual(ValueError, ssm_interpreter.compiler("test6.txt"))
    def test_7(self):
      self.assertEqual(15, ssm_interpreter.compiler("test7.txt"))
    def test_8(self):
      self.assertEqual('\0', ssm_interpreter.compiler("test8.txt"))

    def test_9(self):
      self.assertEqual(ValueError, ssm_interpreter.compiler("test9.txt"))
    def test_10(self):
      self.assertEqual(50, ssm_interpreter.compiler("test10.txt"))



if __name__ == '__main__':
    unittest.main()
