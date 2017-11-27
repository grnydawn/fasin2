from context import fasin
from fasin import prep
import unittest, sys, os, shutil

here = os.path.dirname(os.path.realpath(__file__))
#prog = os.path.join(here, 'caxpy.f')
prog = os.path.join(here, 'inc.f90')
#prog = os.path.join(here, 'add0.f90')

class TestParser(unittest.TestCase):

    def test_prep(self):
        preprocessed = prep(prog)
        return preprocessed

    def _test_parse(self):
        preprocessed = self._test_prep()
        tree = parse(preprocessed)
        #print(sys.stdout)

if __name__ == '__main__':
    unittest.main.main()
