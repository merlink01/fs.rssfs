# coding: utf-8
from __future__ import absolute_import
#~ from __future__ import unicode_literals

from .rssfs import RSSFS
#~ from .opener import ExchangeOpener
__all__ = ['RSSFS']

__license__ = ""
__copyright__ = ""
__author__ = ""
__version__ = 'dev'

# Dynamically get the version of the installed module
#~ try:
    #~ import pkg_resources
    #~ __version__ = pkg_resources.get_distribution(__name__).version
#~ except Exception: # pragma: no cover
    #~ pkg_resources = None
#~ finally:
    #~ del pkg_resources
