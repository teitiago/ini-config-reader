Python Configuration Reader
===========================

This is a simple project to read python configurations from INI files.
Has the following features:

-  It uses the Singleton pattern to configure the reader only once and
   used it across an application.
-  Reloads the configurations when the configuration file is changed.
-  Read OS variables as Strings, e.g., '%(LANG)s'
-  The configurations are automatically converted to a python data type
-  Collect a configuration section as a dictionary

The available data types are: - Strings, surrounded by '' or "" -
Integers - Floats - Lists, [1,2,3] - Dictionaries, {'test': {'is\_dict':
True}}

Installing
----------

To use the config\_reader simple install using pip

.. code:: sh

    $ pip install ini-config-reader

Requirements
~~~~~~~~~~~~

Python3 tested for versions 3.5, 3.6 and 3.7

Usage
-----

The conf\_reader has three class variables, INI\_FILE, RELOAD and
DICT\_CACHE.

+---------------+------------------------------------------------------------------------------------------------+
| Variable      | Description                                                                                    |
+===============+================================================================================================+
| INI\_FILE     | Path to the file that contains the configurations                                              |
+---------------+------------------------------------------------------------------------------------------------+
| RELOAD        | Set if the INI file should be reloaded when changes are detected                               |
+---------------+------------------------------------------------------------------------------------------------+
| DICT\_CACHE   | When collecting the section as dictionary store it in a dict to avoid processing the reading   |
+---------------+------------------------------------------------------------------------------------------------+

Regular usage
~~~~~~~~~~~~~

Since the config\_reader implements the singleton pattern the user only
needs to configure the INI\_File once. Then the get method and
get\_section\_dict can be used as static methods.

.. code:: python

    from conf_reader import ConfReader

    ConfReader('/etc/configuration/my_config.ini')
    ConfReader.get('Section_1', 'configuration_1')  # Can be used in different modules

Decorator
~~~~~~~~~

The config\_reader uses a decorator to inject configuration in
functions. To use it the INI\_FILE must be already configured and a
config variable must exist in the function's signature.

.. code:: python

    from conf_reader import ConfReader, read_conf

    @read_conf("SECTION_1", 'config_2')
    def read_with_arguments(*args, config, **kwargs):
        pass

    ConfReader('/etc/configuration/my_config.ini')
    read_with_arguments()

License
-------

This project is licensed under the MIT License - see the
`LICENSE.txt <LICENSE.txt>`__ file for details
