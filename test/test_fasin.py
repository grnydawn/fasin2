from context import fasin
from fasin import prep, parse
import unittest, sys, os, shutil

here = os.path.dirname(os.path.realpath(__file__))
prog = os.path.join(here, 'end.f90')
#prog = os.path.join(here, 'caxpy.f')
#prog = os.path.join(here, 'inc.f90')
#prog = os.path.join(here, 'add0.f90')

class TestParser(unittest.TestCase):

    def _test_prep(self):
        return prep(prog)

    def test_parse(self):
        source, strmap, cmtmap = self._test_prep()
        tree = parse(source, strmap, cmtmap)
        print(source)
        print(str(tree))
        assert source == str(tree)

if __name__ == '__main__':
    unittest.main.main()
