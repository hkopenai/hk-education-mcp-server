import unittest
from tests.test_tool_primary_schools_enrolment import TestStudentEnrolment

def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestStudentEnrolment))
    return suite

if __name__ == '__main__':
    runner = unittest.TextTestRunner(verbosity=2)
    test_suite = suite()
    runner.run(test_suite)
