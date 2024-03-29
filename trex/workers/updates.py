# -*- coding: utf-8 -*-
#
# Copyright © TRex Project Contributors
# Licensed under the terms of the MIT License
# (see trex/__init__.py for details)

# Standard library imports
import json
import ssl

# Third party imports
from qtpy.QtCore import QObject, Signal

# Local imports
from trex import __version__
from trex.config.base import _
from trex.utils.programs import check_version, is_stable_version


from urllib.request import urlopen
from urllib.error import URLError, HTTPError


class WorkerUpdates(QObject):
    """
    Worker that checks for releases using the Github API without blocking the
    TRex user interface, in case of connections issues.
    """
    sig_ready = Signal()

    def __init__(self, parent, startup):
        QObject.__init__(self)
        self._parent = parent
        self.error = None
        self.latest_release = None
        self.startup = startup

    def check_update_available(self, version, releases):
        """Checks if there is an update available.

        It takes as parameters the current version of TRex and a list of
        valid cleaned releases in chronological order (what github api returns
        by default). Example: ['2.3.4', '2.3.3' ...]
        """
        if is_stable_version(version):
            # Remove non stable versions from the list
            releases = [r for r in releases if is_stable_version(r)]

        latest_release = releases[0]

        if version.endswith('dev'):
            return (False, latest_release)

        return (check_version(version, latest_release, '<'), latest_release)

    def start(self):
        """Main method of the WorkerUpdates worker"""
        self.url = 'https://api.github.com/repos/novaya/trex/releases'
        self.update_available = False
        self.latest_release = __version__

        error_msg = None

        try:
            if hasattr(ssl, '_create_unverified_context'):
                # Fix for issue # 2685 [Works only with Python >=2.7.9]
                # More info: https://www.python.org/dev/peps/pep-0476/#opting-out
                context = ssl._create_unverified_context()
                page = urlopen(self.url, context=context)
            else:
                page = urlopen(self.url)
            try:
                data = page.read()

                # Needed step for python3 compatibility
                if not isinstance(data, str):
                    data = data.decode()

                data = json.loads(data)
                releases = [item['tag_name'].replace('v', '') for item in data]
                version = __version__

                result = self.check_update_available(version, releases)
                self.update_available, self.latest_release = result
            except Exception:
                error_msg = _('Unable to retrieve information.')
        except HTTPError:
            error_msg = _('Unable to retrieve information.')
        except URLError:
            error_msg = _('Unable to connect to the internet. <br><br>Make '
                          'sure the connection is working properly.')
        except Exception:
            error_msg = _('Unable to check for updates.')

        # Don't show dialog when starting up trex and an error occur
        if not (self.startup and error_msg is not None):
            self.error = error_msg
            self.sig_ready.emit()
