'''
Created on Feb 2, 2023

@author: Caleb
'''
import unittest
import Calculator as calc
class TestCalc(unittest.TestCase):

    def testSub1(self):
        self.assertEqual(1, calc.performSub(2, 1), "Bug in implementation. Results should be 1.")    

    def testSub2(self):
        self.assertEqual(10, calc.performSub(20, 10), "Bug in implementation. Results should be 1.")    
# Regular Path Test

    def test010_IntegerMultiplication(self):
        x = 3
        y = -2
        expected = -6
        actual = calc.performMult(x, y)
        self.assertEqual(expected, actual, "bug in implementation. Result should be -6")
    
    def test020_FloatMultiplication(self):
        x = 2.345
        y = -6.3356
        expected = -14.856982
        actual = calc.performMult(x, y)
        precision = 7
        self.assertAlmostEqual(expected, actual, precision,"bug in implementation. Result should be -14.856982")
    
    def test030_IntFloatMultiplication(self):
        x = 2
        y = -12.356
        expected = -24.712
        actual = calc.performMult(x, y)
        self.assertEqual(expected, actual, "bug in implementation. Result should be -24.712")

# Error Path Test

    def test910_NonIntegerInputs(self):
        x = "X"
        y = "Y"
        expected = "Must input two valid numbers (x, y)"
        actual = calc.performMult(x, y)
        self.assertEqual(expected, actual, "bug in implementation. Result should be 'Must input two valid numbers (x, y)'")
    
    def test920_MissingInputs(self):
        expected = "Must input two valid numbers (x, y)"
        actual = calc.performMult()
        self.assertEqual(expected, actual, "bug in implementation. Result should be 'Must input two valid numbers (x, y)'")


# Regular Path Test
    def test010_IntegerDivision(self):
        x = -5839
        y = 330
        expected = -17.69393939394
        actual = calc.performDiv(x, y)
        precision = 11
        self.assertAlmostEqual(expected, actual, precision,"bug in implementation. Result should be -17.69393939394")
    
    def test020_FloatDivision(self):
        x = 77.46
        y = 582.8
        expected = 0.13291008922
        actual = calc.performDiv(x, y)
        precision = 11
        self.assertAlmostEqual(expected, actual, precision,"bug in implementation. Result should be 0.13291008922")
    
    def test030_IntFloatDivision(self):
        x = 1192
        y = 2.55
        expected = 467.45098039216
        actual = calc.performDiv(x, y)
        precision = 11
        self.assertAlmostEqual(expected, actual, precision, "bug in implementation. Result should be 467.45098039216")

# Error Path Test
    
    def test930_DivideByZero(self):
        x = 7789379
        y = 0
        expected = "Divisor cannot be zero"
        actual = calc.performDiv(x, y)
        self.assertEqual(expected, actual, "bug in implementation. Result should be 'Divisor cannot be zero'")

if __name__ == '__main__':
    unittest.main()
