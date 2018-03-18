import unittest

from pkg_resources import resource_filename as rf

from conf_reader.reader import read_conf, ConfReader
from tests import ReaderTestCase


class DecoratorTC(ReaderTestCase):
    """
    Test case to validate all decorator operations.

    Currently it test the read_conf decorator that allows to read
    a configuration and passe it into a function as config argument.
    """

    def test_read_config(self):
        """
        Test the decorator with no arguments involved.
        """

        @read_conf("SECTION_1", 'config_2')
        def read_decorator(config):
            self.assertEqual(config, "Literals")

        read_decorator()

    def test_read_with_argument(self):
        """
        Test the decorator when a function has arguments.
        It validates the arguments remain unchanged.

        The config argument must be placed as last argument of the function.
        """

        @read_conf("SECTION_1", 'config_2')
        def read_with_arguments(arg_1, arg_2, config):
            self.assertEqual(config, "Literals")
            # Check the remaining variables are unchanged
            self.assertEqual(arg_1, 1)
            self.assertEqual(arg_2, 2)

        read_with_arguments(1, 2)

    def test_read_with_argument_list(self):
        """
        Test the decorator when a function has unknown arguments.
        It validates the arguments remain unchanged.

        The config argument must be placed as last argument of the function.
        """

        @read_conf("SECTION_1", 'config_2')
        def read_with_arguments(arg_1, *args, config):
            self.assertEqual(config, "Literals")
            # Check the remaining variables are unchanged
            self.assertEqual(arg_1, 1)
            self.assertEqual(args[0], 2)

        read_with_arguments(1, 2)

    def test_read_with_keyword_argument(self):
        """
        Test the decorator when a function as both arguments and keyword arguments.
        It validates the arguments remain unchanged.

        The config must be placed between arguments and keyword arguments.
        """

        @read_conf("SECTION_1", 'config_2')
        def read_with_keyword_argument(arg_1, *args, config, test='test'):
            self.assertEqual(config, "Literals")
            # Check the remaining variables are unchanged
            self.assertEqual(arg_1, 1)
            self.assertEqual(args[0], 2)
            self.assertEqual(test, 'literal')

        read_with_keyword_argument(1, 2, test='literal')

    def test_read_with_force_reload(self):
        """
        Test the decorator when a function as both arguments and keyword arguments.
        It validates the arguments remain unchanged.

        The config must be placed between arguments and keyword arguments.
        """

        @read_conf("SECTION_1", 'config_4')
        def read_argument(config):
            self.assertEqual(config, 10.5)

        @read_conf("SECTION_1", 'config_4', force_reload=False)
        def read_argument_force(config):
            self.assertEqual(config, 15)

        read_argument()
        ConfReader().change_config_file(rf(__name__, 'data/test_file_2.ini'))  # Loads different ini file
        read_argument_force()


if __name__ == '__main__':
    unittest.main()
