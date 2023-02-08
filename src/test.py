import unittest, sys, os
# current_dir = os.path.dirname(os.path.abspath(__file__))
# top_level_dir = os.path.abspath(os.path.join(current_dir, '..'))
# sys.path.insert(0, top_level_dir)
from src import ssm_interpreter

class TestSSMFiles(unittest.TestCase):
    def test_0(self):
      self.assertEqual(FileNotFoundError, ssm_interpreter.compiler("src/tests/test-1.asm"))
  
    def test_1(self):
      self.assertEqual(30, ssm_interpreter.compiler("src/tests/test1.asm"))
    def test_2(self):
      self.assertEqual(60, ssm_interpreter.compiler("src/tests/test2.asm"))
    def test_3(self):
      self.assertEqual(60, ssm_interpreter.compiler("src/tests/test3.asm"))
    def test_4(self):
      self.assertEqual(25, ssm_interpreter.compiler("src/tests/test4.asm"))
      
    def test_5(self):
      self.assertEqual(ValueError, ssm_interpreter.compiler("src/tests/test5.asm"))
    def test_6(self):
      self.assertEqual(ValueError, ssm_interpreter.compiler("src/tests/test6.asm"))
    def test_7(self):
      self.assertEqual(15, ssm_interpreter.compiler("src/tests/test7.asm"))
    def test_8(self):
      self.assertEqual('\0', ssm_interpreter.compiler("src/tests/test8.asm"))

    def test_9(self):
      self.assertEqual(ValueError, ssm_interpreter.compiler("src/tests/test9.asm"))
    def test_10(self):
      self.assertEqual(10, ssm_interpreter.compiler("src/tests/test10.asm"))
    def test_11(self):
      self.assertEqual(ValueError, ssm_interpreter.compiler("src/tests/test11.asm"))
    def test_12(self):
      self.assertEqual(ValueError, ssm_interpreter.compiler("src/tests/test12.asm"))
    
    def test_13(self):
      self.assertEqual(220, ssm_interpreter.compiler("src/tests/test13.asm"))
    def test_14(self):
      self.assertEqual(ArithmeticError, ssm_interpreter.compiler("src/tests/test14.asm"))
    def test_15(self):
      self.assertEqual(NameError, ssm_interpreter.compiler("src/tests/test15.asm"))
    def test_16(self):
      self.assertEqual(LookupError, ssm_interpreter.compiler("src/tests/test16.asm"))



if __name__ == '__main__':
    unittest.main()
