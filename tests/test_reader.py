from configparser import NoSectionError, NoOptionError
from unittest import main
from unittest.mock import patch

from pkg_resources import resource_filename as rf

from conf_reader import ConfReader
from tests import ReaderTestCase


class ReadeActionsTC(ReaderTestCase):

    def test_reader_valid_sections(self):
        """
        Validates if the reader is working as expected.
        Asserts all types from a specific section of the file
        """
        self.assertTrue(isinstance(ConfReader.get('SECTION_1', 'config_1'), str))
        self.assertTrue(isinstance(ConfReader.get('SECTION_1', 'config_2'), str))
        self.assertTrue(isinstance(ConfReader.get('SECTION_1', 'config_3'), int))
        self.assertTrue(isinstance(ConfReader.get('SECTION_1', 'config_4'), float))

    def test_invalid_sections(self):
        """
        Validates if NoSectionError is raised when the section is not available,
        both on the get and get as dict
        """
        self.assertRaises(NoSectionError, lambda: ConfReader.get('SECTION_X', 'config_x'))
        self.assertRaises(NoSectionError, lambda: ConfReader.get_section_dict('SECTION_X'))

    def test_invalid_option(self):
        """
        Validates if NoOptionError is raised when the option is not available
        """
        self.assertRaises(NoOptionError, lambda: ConfReader.get('SECTION_1', 'config_x'))

    def test_invalid_config_file(self):
        """
        Validates if FileNotFoundError is raised when loading the configuration
        """
        ConfReader.INI_FILE = rf(__name__, 'data/invalid_test.ini')  # Loads different ini file
        self.assertRaises(FileNotFoundError, lambda: ConfReader.get('X', 'y'))

    def test_get_dict(self):
        """
        Validates if the parser can collect a dictionary as a configuration
        """
        config = ConfReader.get('SECTION_2', 'config_6')
        self.assertTrue(isinstance(config, dict))

    def test_get_list(self):
        """
        Validates if te parser can collect a list as a configuration
        """
        config = ConfReader.get('SECTION_2', 'config_5')
        self.assertTrue(isinstance(config, list))
        self.assertEqual(config, [1, 2, 3, 4, 5])

    def test_get_section_dict(self):
        """
        Validates if the complete section can be collected ina python format
        """
        section_1 = ConfReader.get_section_dict('SECTION_1')
        self.assertTrue(isinstance(section_1, dict))

        section_2 = ConfReader.get_section_dict('SECTION_2')
        self.assertTrue(isinstance(section_2, dict))
        self.assertTrue(isinstance(section_2.get('config_6'), dict))
        self.assertTrue(isinstance(section_2.get('config_5'), list))

    @patch('conf_reader.os.path.getmtime')
    def test_file_reload(self, get_time):
        """
        Validates if the reload is successfully done.
        This is tested by forcing a new INI file
        """
        base_time = ConfReader.__INI_FILE_TIME__
        get_time.return_value = base_time

        self.assertEqual(ConfReader.get('SECTION_1', 'config_4'), 10.5)
        ConfReader.INI_FILE = rf(__name__, 'data/test_file_2.ini')  # Loads different ini file
        get_time.return_value = base_time + 15  # Force the modification time higher then the original

        self.assertEqual(ConfReader.get('SECTION_1', 'config_4'), 15)

    @patch('conf_reader.os.path.getmtime')
    def test_reload_parameter(self, get_time):
        """
        Validates the force_reload option when the RELOAD is False.
        This is tested by forcing a new INI file
        """
        base_time = ConfReader.__INI_FILE_TIME__
        get_time.return_value = base_time

        self.assertEqual(ConfReader.get('SECTION_1', 'config_4'), 10.5)
        ConfReader.INI_FILE = rf(__name__, 'data/test_file_2.ini')  # Loads different ini file
        ConfReader.RELOAD = False
        get_time.return_value = base_time + 15  # Force the modification time higher then the original

        self.assertEqual(ConfReader.get('SECTION_1', 'config_4', force_reload=True), 15)

    def test_file_not_reloaded(self):
        """
        Validates if the configuration remain after an unsuccessfully reload operation.
        This is done by changing the file and setting the reload as False.
        """
        self.assertEqual(ConfReader.get('SECTION_1', 'config_4'), 10.5)
        ConfReader.INI_FILE = rf(__name__, 'data/test_file_2.ini')  # Loads different ini file
        ConfReader.RELOAD = False
        self.assertEqual(ConfReader.get('SECTION_1', 'config_4'), 10.5)

    @patch('conf_reader.os.path.getmtime')
    def test_unmodified_change_date_dont_reload(self, get_time=None):
        """
        Validates if the configuration remain after an unsuccessfully force reload operation.
        This is done by changing the file and setting the reload as False.
        """
        base_time = ConfReader.__INI_FILE_TIME__
        get_time.return_value = base_time

        self.assertEqual(ConfReader.get('SECTION_1', 'config_4'), 10.5)
        ConfReader.INI_FILE = rf(__name__, 'data/test_file_2.ini')  # Loads different ini file

        # Assert same config with RELOAD on even with file change
        self.assertEqual(ConfReader.get('SECTION_1', 'config_4', force_reload=True), 10.5)


if __name__ == '__main__':
    main()  # Unittest main
