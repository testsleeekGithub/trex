# -*- coding: utf-8 -*-
#
# Copyright © TRex Project Contributors
# Licensed under the terms of the MIT License
# (see trex/__init__.py for details)

"""
TRex base configuration management

This file only deals with non-GUI configuration features
(in other words, we won't import any PyQt object here, avoiding any
sip API incompatibility issue in trex's non-gui modules)
"""

import codecs
import locale
import os.path as osp
import os
import shutil
import sys

# Local imports
from trex.utils import encoding
from trex.py3compat import (is_unicode, TEXT_TYPES, INT_TYPES,
                              to_text_string, is_text_string)


#==============================================================================
# Only for development
#==============================================================================
# To activate/deactivate certain things for development
# TREX_DEV is (and *only* has to be) set in bootstrap.py
DEV = os.environ.get('TREX_DEV')

# For testing purposes
# TREX_TEST can be set using the --test option of bootstrap.py
TEST = os.environ.get('TREX_TEST')


# To do some adjustments for pytest
# This env var is defined in runtests.py
PYTEST = os.environ.get('TREX_PYTEST')


#==============================================================================
# Debug helpers
#==============================================================================
# This is needed after restarting and using debug_print
STDOUT = sys.stdout
STDERR = sys.stderr
def _get_debug_env():
    debug_env = os.environ.get('TREX_DEBUG', '')
    if not debug_env.isdigit():
        debug_env = bool(debug_env)
    return int(debug_env)    
DEBUG = _get_debug_env()

def debug_print(*message):
    """Output debug messages to stdout"""
    if DEBUG:
        ss = STDOUT

        # This is needed after restarting and using debug_print
        for m in message:
            ss.buffer.write(str(m).encode('utf-8'))
        print('', file=ss)



#==============================================================================
# Configuration paths
#==============================================================================
# TRex settings dir
if sys.platform.startswith('linux'):
    SUBFOLDER = 'trex-py3'
else:
    SUBFOLDER = '.trex-py3'


def get_home_dir():
    """
    Return user home directory
    """
    try:
        # expanduser() returns a raw byte string which needs to be
        # decoded with the codec that the OS is using to represent file paths.
        path = encoding.to_unicode_from_fs(osp.expanduser('~'))
    except:
        path = ''
    for env_var in ('HOME', 'USERPROFILE', 'TMP'):
        if osp.isdir(path):
            break
        # os.environ.get() returns a raw byte string which needs to be
        # decoded with the codec that the OS is using to represent environment
        # variables.
        path = encoding.to_unicode_from_fs(os.environ.get(env_var, ''))
    if path:
        return path
    else:
        raise RuntimeError('Please define environment variable $HOME')


def get_conf_path(filename=None):
    """Return absolute path for configuration file with specified filename"""
    # This makes us follow the XDG standard to save our settings
    # on Linux, as it was requested on Issue 2629
    if sys.platform.startswith('linux'):
        xdg_config_home = os.environ.get('XDG_CONFIG_HOME', '')
        if not xdg_config_home:
            xdg_config_home = osp.join(get_home_dir(), '.config')
        if not osp.isdir(xdg_config_home):
            os.makedirs(xdg_config_home)
        conf_dir = osp.join(xdg_config_home, SUBFOLDER)
    else:
        conf_dir = osp.join(get_home_dir(), SUBFOLDER)
    if not osp.isdir(conf_dir):
        os.mkdir(conf_dir)
    if filename is None:
        return conf_dir
    else:
        return osp.join(conf_dir, filename)
        

def get_module_path(modname):
    """Return module *modname* base path"""
    return osp.abspath(osp.dirname(sys.modules[modname].__file__))


def get_module_data_path(modname, relpath=None, attr_name='DATAPATH'):
    """Return module *modname* data path
    Note: relpath is ignored if module has an attribute named *attr_name*
    
    Handles py2exe/cx_Freeze distributions"""
    datapath = getattr(sys.modules[modname], attr_name, '')
    if datapath:
        return datapath
    else:
        datapath = get_module_path(modname)
        parentdir = osp.join(datapath, osp.pardir)
        if osp.isfile(parentdir):
            # Parent directory is not a directory but the 'library.zip' file:
            # this is either a py2exe or a cx_Freeze distribution
            datapath = osp.abspath(osp.join(osp.join(parentdir, osp.pardir),
                                            modname))
        if relpath is not None:
            datapath = osp.abspath(osp.join(datapath, relpath))
        return datapath


def get_module_source_path(modname, basename=None):
    """Return module *modname* source path
    If *basename* is specified, return *modname.basename* path where 
    *modname* is a package containing the module *basename*
    
    *basename* is a filename (not a module name), so it must include the
    file extension: .py or .pyw
    
    Handles py2exe/cx_Freeze distributions"""
    srcpath = get_module_path(modname)
    parentdir = osp.join(srcpath, osp.pardir)
    if osp.isfile(parentdir):
        # Parent directory is not a directory but the 'library.zip' file:
        # this is either a py2exe or a cx_Freeze distribution
        srcpath = osp.abspath(osp.join(osp.join(parentdir, osp.pardir),
                                       modname))
    if basename is not None:
        srcpath = osp.abspath(osp.join(srcpath, basename))
    return srcpath


def is_py2exe_or_cx_Freeze():
    """Return True if this is a py2exe/cx_Freeze distribution of TRex"""
    return osp.isfile(osp.join(get_module_path('trex'), osp.pardir))


SCIENTIFIC_STARTUP = get_module_source_path('trex', 'scientific_startup.py')


#==============================================================================
# Image path list
#==============================================================================
IMG_PATH = []
def add_image_path(path):
    if not osp.isdir(path):
        return
    global IMG_PATH
    IMG_PATH.append(path)
    for dirpath, dirnames, _filenames in os.walk(path):
        for dirname in dirnames:
            IMG_PATH.append(osp.join(dirpath, dirname))

add_image_path(get_module_data_path('trex', relpath='images'))

def get_image_path(name, default="not_found.png"):
    """Return image absolute path"""
    for img_path in IMG_PATH:
        full_path = osp.join(img_path, name)
        if osp.isfile(full_path):
            return osp.abspath(full_path)
    if default is not None:
        img_path = osp.join(get_module_path('trex'), 'images')
        return osp.abspath(osp.join(img_path, default))


#==============================================================================
# Translations
#==============================================================================
LANG_FILE = get_conf_path('langconfig')
DEFAULT_LANGUAGE = 'en'

# This needs to be updated every time a new language is added to trex, and is
# used by the Preferences configuration to populate the Language QComboBox
LANGUAGE_CODES = {'en': u'English',
                  'fr': u'Français',
                  'es': u'Español',
                  'pt_BR': u'Português',
                  'ru': u'Русский',
                  'ja': u'日本語'
                  }

# Disabled languages (because their translations are outdated)
DISABLED_LANGUAGES = []

def get_available_translations():
    """
    List available translations for trex based on the folders found in the
    locale folder. This function checks if LANGUAGE_CODES contain the same
    information that is found in the 'locale' folder to ensure that when a new
    language is added, LANGUAGE_CODES is updated.
    """
    locale_path = get_module_data_path("trex", relpath="locale",
                                       attr_name='LOCALEPATH')
    listdir = os.listdir(locale_path)
    langs = [d for d in listdir if osp.isdir(osp.join(locale_path, d))]
    langs = [DEFAULT_LANGUAGE] + langs

    # Remove disabled languages
    langs = list( set(langs) - set(DISABLED_LANGUAGES) )

    # Check that there is a language code available in case a new translation
    # is added, to ensure LANGUAGE_CODES is updated.
    for lang in langs:
        if lang not in LANGUAGE_CODES:
            error = _('Update LANGUAGE_CODES (inside config/base.py) if a new '
                      'translation has been added to TRex')
            raise Exception(error)
    return langs


def get_interface_language():
    """
    If TRex has a translation available for the locale language, it will
    return the version provided by TRex adjusted for language subdifferences,
    otherwise it will return DEFAULT_LANGUAGE.

    Example:
    1.) TRex provides ('en',  'fr', 'es' and 'pt_BR'), if the locale is
    either 'en_US' or 'en' or 'en_UK', this function will return 'en'

    2.) TRex provides ('en',  'fr', 'es' and 'pt_BR'), if the locale is
    either 'pt' or 'pt_BR', this function will return 'pt_BR'
    """

    # Solves issue #3627
    try:
        locale_language = locale.getdefaultlocale()[0]
    except ValueError:
        locale_language = DEFAULT_LANGUAGE

    language = DEFAULT_LANGUAGE

    if locale_language is not None:
        trex_languages = get_available_translations()
        for lang in trex_languages:
            if locale_language == lang:
                language = locale_language
                break
            elif locale_language.startswith(lang) or \
              lang.startswith(locale_language):
                language = lang
                break

    return language


def save_lang_conf(value):
    """Save language setting to language config file"""
    with open(LANG_FILE, 'w') as f:
        f.write(value)


def load_lang_conf():
    """
    Load language setting from language config file if it exists, otherwise
    try to use the local settings if TRex provides a translation, or
    return the default if no translation provided.
    """
    if osp.isfile(LANG_FILE):
        with open(LANG_FILE, 'r') as f:
            lang = f.read()
    else:
        lang = get_interface_language()
        save_lang_conf(lang)

    # Save language again if it's been disabled
    if lang.strip('\n') in DISABLED_LANGUAGES:
        lang = DEFAULT_LANGUAGE
        save_lang_conf(lang)

    return lang


def get_translation(modname, dirname=None):
    """Return translation callback for module *modname*"""
    if dirname is None:
        dirname = modname
    locale_path = get_module_data_path(dirname, relpath="locale",
                                       attr_name='LOCALEPATH')
    # If LANG is defined in ubuntu, a warning message is displayed, so in unix
    # systems we define the LANGUAGE variable.
    language = load_lang_conf()
    if os.name == 'nt':
        os.environ["LANG"] = language      # Works on Windows
    else:
        os.environ["LANGUAGE"] = language  # Works on Linux
 
    import gettext
    try:
        _trans = gettext.translation(modname, locale_path, codeset="utf-8")
        lgettext = _trans.lgettext
        def translate_gettext(x):

            y = lgettext(x)
            if is_text_string(y):
                return y
            else:
                return to_text_string(y, "utf-8")
        return translate_gettext
    except IOError as _e:  # analysis:ignore
        # Not using translations
        def translate_dumb(x):
            if not is_unicode(x):
                return to_text_string(x, "utf-8")
            return x
        return translate_dumb

# Translation callback
_ = get_translation("trex")


#==============================================================================
# Namespace Browser (Variable Explorer) configuration management
#==============================================================================
def get_supported_types():
    """
    Return a dictionnary containing types lists supported by the 
    namespace browser:
    dict(picklable=picklable_types, editable=editables_types)
         
    See:
    get_remote_data function in trex/widgets/variableexplorer/utils/monitor.py
    
    Note:
    If you update this list, don't forget to update doc/variablexplorer.rst
    """
    from datetime import date
    editable_types = [int, float, complex, list, dict, tuple, date
                      ] + list(TEXT_TYPES) + list(INT_TYPES)
    try:
        from numpy import ndarray, matrix, generic
        editable_types += [ndarray, matrix, generic]
    except ImportError:
        pass
    try:
        from pandas import DataFrame, Series, DatetimeIndex
        editable_types += [DataFrame, Series, DatetimeIndex]
    except ImportError:
        pass
    picklable_types = editable_types[:]
    try:
        from trex.pil_patch import Image
        editable_types.append(Image.Image)
    except ImportError:
        pass
    return dict(picklable=picklable_types, editable=editable_types)

# Variable explorer display / check all elements data types for sequences:
# (when saving the variable explorer contents, check_all is True,
#  see widgets/variableexplorer/namespacebrowser.py:NamespaceBrowser.save_data)
CHECK_ALL = False #XXX: If True, this should take too much to compute...

EXCLUDED_NAMES = ['nan', 'inf', 'infty', 'little_endian', 'colorbar_doc',
                  'typecodes', '__builtins__', '__main__', '__doc__', 'NaN',
                  'Inf', 'Infinity', 'sctypes', 'rcParams', 'rcParamsDefault',
                  'sctypeNA', 'typeNA', 'False_', 'True_',]


#==============================================================================
# Mac application utilities
#==============================================================================
MAC_APP_NAME = 'TRex.app'


def running_in_mac_app():
    if sys.platform == "darwin" and MAC_APP_NAME in __file__:
        return True
    else:
        return False


#==============================================================================
# Reset config files
#==============================================================================
SAVED_CONFIG_FILES = ('help', 'onlinehelp', 'path', 'pylint.results',
                      'trex.ini', 'temp.py', 'temp.spydata', 'template.py',
                      'history.py', 'history_internal.py', 'workingdir',
                      '.projects', '.trexproject', '.ropeproject',
                      'monitor.log', 'monitor_debug.log', 'rope.log',
                      'langconfig', 'trex.lock')


def reset_config_files():
    """Remove all config files"""
    print("*** Reset TRex settings to defaults ***", file=STDERR)
    for fname in SAVED_CONFIG_FILES:
        cfg_fname = get_conf_path(fname)
        if osp.isfile(cfg_fname) or osp.islink(cfg_fname):
            os.remove(cfg_fname)
        elif osp.isdir(cfg_fname):
            shutil.rmtree(cfg_fname)
        else:
            continue
        print("removing:", cfg_fname, file=STDERR)
