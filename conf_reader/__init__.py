import configparser
import logging
import os
from ast import literal_eval as le
from functools import wraps

from conf_reader.singleton import Singleton

logger = logging.getLogger(__name__)


# TODO: Read ENV as other formats
# TODO: Support multiple INI Files
# TODO: Correct INI files

def reload(_function_):
    """
    Forces the configurations reload, either because a new INI file was loaded
    or due to real time file reading.

    The reload only happens if the file modification time is recent then the last
    load time.

    :param _function_:
    """

    @wraps(_function_)
    def wrapper(*args, **kwargs):
        if (ConfReader.RELOAD or kwargs.get('force_reload', False)) and os.path.getmtime(
                ConfReader.INI_FILE) > ConfReader.__INI_FILE_TIME__:
            ConfReader().__initialize_dict_cache__()
            ConfReader().change_config_file()
            logger.debug('Config reader reloaded')
        return _function_(*args, **kwargs)

    return wrapper


def read_conf(section, config, force_reload=False):
    """
    Loads a configuration as an input parameter of a function.
    It introduces a keyword argument config in the function

    @read_conf("Section_1", "config_1")
    def test(*args, config, **kwargs)

    """

    def read(_function_):
        @wraps(_function_)
        def wrapper(*args, **kwargs):
            conf = ConfReader.get(section, config, force_reload=force_reload)
            return _function_(*args, config=conf, **kwargs)

        return wrapper

    return read


class ConfReader(metaclass=Singleton):
    """
    Class to read INI files with eval configurations.

    This class allows users to specify the INI file and collect the results

    Its main features:
        - Collect configurations without string defaults
        - Reload the configuration file in every reading
        - Collect Configuration sections as dictionaries
            - Store the dictionaries configurations in a dictionary

    """

    # INI file with configurations to be loaded
    INI_FILE = None
    __INI_FILE_TIME__ = None

    # Variable that forces to reload the INI file every time a configuration is loaded
    RELOAD = True

    # Stores the dictionary reading in a dictionary {SECTION: {CONFIGURATIONS}}
    # This avoids processing the section more then once
    DICT_CACHE = False

    def __init__(self, ini_file=None):
        """
        Loads the ConfReader. It uses a os.environ to allow ENV variables reading,
        as the format '%()'.

        NOTE: the ENV variable must be Strings
        """
        logger.debug('Config reader initialization')

        self.config = configparser.ConfigParser(os.environ, allow_no_value=True)
        self.config_dict = configparser.ConfigParser(allow_no_value=True)  # config dict allows to read all sections

        self.change_config_file(ini_file)

        self.__initialize_dict_cache__()

        logger.info('Config reader successfully initialized with {}'.format(ConfReader.INI_FILE))

    def change_config_file(self, ini_file=None):
        if ini_file:
            ConfReader.INI_FILE = ini_file
        self.read_conf_file(self.config)
        self.read_conf_file(self.config_dict)

    @staticmethod
    def read_conf_file(config):
        """
        Read the specified INI_FILE. This clears every loaded configuration.
        :raises:
                FileNotFoundError, when the INI_FILE is not a valid path
        """
        if not os.path.exists(ConfReader.INI_FILE):
            logger.exception("Provided file {} don't exist".format(ConfReader.INI_FILE), exc_info=False)
            raise FileNotFoundError()

        with open(ConfReader.INI_FILE) as _file_:
            config.clear()
            config.read_file(_file_)

        # Store the reader modification time to automatic reload
        ConfReader.__INI_FILE_TIME__ = os.path.getmtime(ConfReader.INI_FILE)
        logger.debug('Ini file successfully loaded')

    def __initialize_dict_cache__(self):
        """
        Restores the dict cache
        """
        logger.debug('Dict cache cleared')
        self.cache = {}

    @staticmethod
    @reload
    def get(section, config, force_reload=False):
        """
        Collect the specified configuration in the provided section.
        This function evaluates the type of the variable and return the correct type.

        It is valid and tested for Lists [], Dicts {}, Strings, Floats and Integers.

        :param section: the Section to collect the values
        :param config: the configuration to collect
        :param force_reload: variable used by the reload decorator to force the INI File reload.
        :return: The configuration as the correct type
        :raises:
                configparser.NoSectionError, when the provided section is not loaded
                configparser.NoOptionError, when the provided config is not loaded
                configparser.InterpolationMissingOptionError, when the OS ENV doesnt exist
                ValueError: malformed node or string, when the OS ENV are not surrounded by ''
        """
        self = ConfReader.instance
        return le(self.config.get(section, config))

    @staticmethod
    @reload
    def get_section_dict(section, force_reload=False):
        """
        Collect configuration as a dictionary.
        If the DICT_CACHE is active the reader will store the configurations on a dictionary
        with the section as key and load it directly next time is required.

        :param section: the Section to collect the values
        :param force_reload: variable used by the reload decorator to force the INI File reload.
                            When used in get_section_dict all cache is cleared
        :return: Dictionary with the section and its values
        :raises:
                configparser.NoSectionError, when the provided section is not loaded
        """
        self = ConfReader.instance
        if section not in self.config:
            logger.exception('Provided section {} is not valid'.format(section), exc_info=False)
            raise configparser.NoSectionError(section)

        # Check Cache for dict
        if ConfReader.DICT_CACHE and section in self.cache.keys():
            return self.cache.get(section)

        # Collect all configurations
        configs_list = self.config_dict.items(section, raw=True)
        configs = dict()

        # Parse configurations to dictionary
        for key, value in configs_list:
            configs[key] = self.get(section, key)

        # Store configuration in memory
        if ConfReader.DICT_CACHE:
            self.cache[section] = configs

        return configs

