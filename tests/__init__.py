from unittest import TestCase

from pkg_resources import resource_filename as rf

from conf_reader.reader import ConfReader


class ReaderTestCase(TestCase):
    """
    Conf Reader test case.

    Forces the loading of a specific INI file on the beginning of each test
    """

    INI_TEST_FILE = 'data/test_file.ini'

    def setUp(self):
        """
        Initialize test case with a preconfigured ini file
        """
        ConfReader.RELOAD = True
        ConfReader.DICT_CACHE = False
        ConfReader(rf(__name__, ReaderTestCase.INI_TEST_FILE))  # The ConfReader must be initialized

    def tearDown(self):
        ConfReader.destroy()  # Remove the created instance
