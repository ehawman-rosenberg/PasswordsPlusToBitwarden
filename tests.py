import unittest
from pp2bw import CustomField

class TestCustomClasses(unittest.TestCase):

    def test_linkedId_in_textfield(self):
        with self.assertRaises(ValueError):
            x=CustomField("TextName", 0, "Test",linkedId="Hello")

    def test_linkedId_in_boolfield(self):
        with self.assertRaises(ValueError):
            x=CustomField("TextName", 2, "Test",linkedId="Hello")

    
if __name__ == '__main__':
    unittest.main(verbosity=2)