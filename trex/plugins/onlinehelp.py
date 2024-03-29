# -*- coding: utf-8 -*-
#
# Copyright © TRex Project Contributors
# Licensed under the terms of the MIT License
# (see trex/__init__.py for details)

"""Online Help Plugin"""

# Standard library imports
import os.path as osp

# Third party imports
from qtpy.QtCore import Signal

# Local imports
from trex.config.base import _, get_conf_path
from trex.plugins import TRexPluginMixin
from trex.py3compat import to_text_string
from trex.widgets.pydocgui import PydocBrowser


class OnlineHelp(PydocBrowser, TRexPluginMixin):
    """
    Online Help Plugin
    """
    sig_option_changed = Signal(str, object)
    CONF_SECTION = 'onlinehelp'
    LOG_PATH = get_conf_path(CONF_SECTION)

    def __init__(self, parent):
        self.main = parent
        PydocBrowser.__init__(self, parent)
        TRexPluginMixin.__init__(self, parent)

        # Initialize plugin
        self.initialize_plugin()

        self.register_widget_shortcuts(self.find_widget)

        self.webview.set_zoom_factor(self.get_option('zoom_factor'))
        self.url_combo.setMaxCount(self.get_option('max_history_entries'))
        self.url_combo.addItems( self.load_history() )
        
    #------ Public API ---------------------------------------------------------
    def load_history(self, obj=None):
        """Load history from a text file in user home directory"""
        if osp.isfile(self.LOG_PATH):
            history = [line.replace('\n', '')
                       for line in open(self.LOG_PATH, 'r').readlines()]
        else:
            history = []
        return history
    
    def save_history(self):
        """Save history to a text file in user home directory"""
        open(self.LOG_PATH, 'w').write("\n".join( \
                [to_text_string(self.url_combo.itemText(index))
                 for index in range(self.url_combo.count())] ))

    #------ TRexPluginMixin API ---------------------------------------------
    def visibility_changed(self, enable):
        """DockWidget visibility has changed"""
        TRexPluginMixin.visibility_changed(self, enable)
        if enable and not self.is_server_running():
            self.initialize()
    
    #------ TRexPluginWidget API ---------------------------------------------
    def get_plugin_title(self):
        """Return widget title"""
        return _('Online help')
    
    def get_focus_widget(self):
        """
        Return the widget to give focus to when
        this plugin's dockwidget is raised on top-level
        """
        self.url_combo.lineEdit().selectAll()
        return self.url_combo
        
    def closing_plugin(self, cancelable=False):
        """Perform actions before parent main window is closed"""
        self.save_history()
        self.set_option('zoom_factor', self.webview.get_zoom_factor())
        return True
        
    def refresh_plugin(self):
        """Refresh widget"""
        pass
    
    def get_plugin_actions(self):
        """Return a list of actions related to plugin"""
        return []
    
    def register_plugin(self):
        """Register plugin in TRex's main window"""
        self.main.add_dockwidget(self)
        