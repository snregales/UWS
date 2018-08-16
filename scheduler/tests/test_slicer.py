from django.test import TestCase
from ..utils import Slicer


class SlicerTestCases(TestCase):
    @classmethod
    def setUpClass(cls):
        print('-----' + cls.__name__ + '-----')
        cls.lizt = cls.create_list(24)

    @classmethod
    def tearDownClass(cls):
        print('')

    def setUp(self):
        self.slicer = Slicer()

    @staticmethod
    def create_list(n):
        return list(str(chr(65+i)) for i in range(n))

    def test_assistant(self):
        print('assistant')
        self.slicer.set_slicer_var(self.lizt[:10], self.lizt[:12], 3)
        self.assertEqual(
            self.slicer._assistant(6, 6),
            ([['A', 'C', 'E'], ['B', 'D', 'F'], ['G', 'H', 'I', 'J']],
             [['A', 'C', 'E'], ['B', 'D', 'F'], ['G', 'H', 'I', 'J', 'K', 'L']]))
        self.slicer.set_slicer_var(self.lizt[:11], self.lizt[:15], 3)
        self.assertEqual(
            self.slicer._assistant(8, 12),
            ([['A', 'C', 'E', 'G'], ['B', 'D', 'F', 'H'], ['I', 'J', 'K']],
             [['A', 'C', 'E', 'G', 'I', 'K'],
              ['B', 'D', 'F', 'H', 'J', 'L'],
              ['M', 'N', 'O']]))
        self.slicer.set_slicer_var(self.lizt[:13], self.lizt[:15], 4)
        self.assertEqual(
            self.slicer._assistant(9, 9),
            ([['A', 'D', 'G'], ['B', 'E', 'H'], ['C', 'F', 'I'], ['J', 'K', 'L', 'M']],
             [['A', 'D', 'G'],
              ['B', 'E', 'H'],
              ['C', 'F', 'I'],
              ['J', 'K', 'L', 'M', 'N', 'O']]))
        self.slicer.set_slicer_var(self.lizt[:14], self.lizt[:18], 4)
        self.assertEqual(
            self.slicer._assistant(8, 12),
            ([['A', 'C', 'E', 'G'], ['B', 'D', 'F', 'H'], ['I', 'K', 'M'], ['J', 'L', 'N']],
             [['A', 'C', 'E', 'G', 'I', 'K'],
              ['B', 'D', 'F', 'H', 'J', 'L'],
              ['M', 'O', 'Q'],
              ['N', 'P', 'R']]))
        self.slicer.set_slicer_var(self.lizt[:15], self.lizt[:21], 4)
        self.assertEqual(
            self.slicer._assistant(12, 18),
            ([['A', 'D', 'G', 'J'],
              ['B', 'E', 'H', 'K'],
              ['C', 'F', 'I', 'L'],
              ['M', 'N', 'O']],
             [['A', 'D', 'G', 'J', 'M', 'P'],
              ['B', 'E', 'H', 'K', 'N', 'Q'],
              ['C', 'F', 'I', 'L', 'O', 'R'],
              ['S', 'T', 'U']]))

    def test_manager(self):
        print('manager')
        self.slicer.set_slicer_var(self.lizt[:8], self.lizt[:12], 2)
        self.assertEqual(
            self.slicer.slicer_manager(),
            ([['A', 'C', 'E', 'G'], ['B', 'D', 'F', 'H']],
             [['A', 'C', 'E', 'G', 'I', 'K'], ['B', 'D', 'F', 'H', 'J', 'L']]))
        self.slicer.set_slicer_var(self.lizt[:9], self.lizt[:9], 3)
        self.assertEqual(
            self.slicer.slicer_manager(),
            ([['A', 'C', 'E'], ['B', 'D', 'F'], ['G', 'H', 'I']],
             [['A', 'C', 'E'], ['B', 'D', 'F'], ['G', 'H', 'I']]))
        self.slicer.set_slicer_var(self.lizt[:10], self.lizt[:12], 3)
        self.assertEqual(
            self.slicer.slicer_manager(),
            ([['A', 'C', 'E'], ['B', 'D', 'F'], ['G', 'H', 'I', 'J']],
             [['A', 'C', 'E'], ['B', 'D', 'F'], ['G', 'H', 'I', 'J', 'K', 'L']]))
        self.slicer.set_slicer_var(self.lizt[:11], self.lizt[:15], 3)
        self.assertEqual(
            self.slicer.slicer_manager(),
            ([['A', 'C', 'E', 'G'], ['B', 'D', 'F', 'H'], ['I', 'J', 'K']],
             [['A', 'C', 'E', 'G', 'I', 'K'],
              ['B', 'D', 'F', 'H', 'J', 'L'],
              ['M', 'N', 'O']]))
        self.slicer.set_slicer_var(self.lizt[:12], self.lizt[:18], 3)
        self.assertEqual(
            self.slicer.slicer_manager(),
            ([['A', 'D', 'G', 'J'], ['B', 'E', 'H', 'K'], ['C', 'F', 'I', 'L']],
             [['A', 'D', 'G', 'J', 'M', 'P'],
              ['B', 'E', 'H', 'K', 'N', 'Q'],
              ['C', 'F', 'I', 'L', 'O', 'R']]))
        self.slicer.set_slicer_var(self.lizt[:13], self.lizt[:15], 4)
        self.assertEqual(
            self.slicer.slicer_manager(),
            ([['A', 'D', 'G'], ['B', 'E', 'H'], ['C', 'F', 'I'], ['J', 'K', 'L', 'M']],
             [['A', 'D', 'G'],
              ['B', 'E', 'H'],
              ['C', 'F', 'I'],
              ['J', 'K', 'L', 'M', 'N', 'O']]))
        self.slicer.set_slicer_var(self.lizt[:14], self.lizt[:18], 4)
        self.assertEqual(
            self.slicer.slicer_manager(),
            ([['A', 'C', 'E', 'G'], ['B', 'D', 'F', 'H'], ['I', 'K', 'M'], ['J', 'L', 'N']],
             [['A', 'C', 'E', 'G', 'I', 'K'],
              ['B', 'D', 'F', 'H', 'J', 'L'],
              ['M', 'O', 'Q'],
              ['N', 'P', 'R']]))
        self.slicer.set_slicer_var(self.lizt[:15], self.lizt[:21], 4)
        self.assertEqual(
            self.slicer.slicer_manager(),
            ([['A', 'D', 'G', 'J'],
              ['B', 'E', 'H', 'K'],
              ['C', 'F', 'I', 'L'],
              ['M', 'N', 'O']],
             [['A', 'D', 'G', 'J', 'M', 'P'],
              ['B', 'E', 'H', 'K', 'N', 'Q'],
              ['C', 'F', 'I', 'L', 'O', 'R'],
              ['S', 'T', 'U']]))
        self.slicer.set_slicer_var(self.lizt[:16], self.lizt[:24], 4)
        self.assertEqual(
            self.slicer.slicer_manager(),
            ([['A', 'E', 'I', 'M'],
              ['B', 'F', 'J', 'N'],
              ['C', 'G', 'K', 'O'],
              ['D', 'H', 'L', 'P']],
             [['A', 'E', 'I', 'M', 'Q', 'U'],
              ['B', 'F', 'J', 'N', 'R', 'V'],
              ['C', 'G', 'K', 'O', 'S', 'W'],
              ['D', 'H', 'L', 'P', 'T', 'X']]))
