import unittest
from common.Instructions import Instructions


class MyTestCase(unittest.TestCase):
    def test_instructions(self):
        instructions = Instructions('materials', 'upload')
        self.assertEqual(True, True)


if __name__ == '__main__':
    unittest.main()
