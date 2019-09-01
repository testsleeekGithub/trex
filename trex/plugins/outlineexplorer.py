# -*- coding: utf-8 -*-
#
# Copyright © TRex Project Contributors
# Licensed under the terms of the MIT License
# (see trex/__init__.py for details)

"""Outline Explorer Plugin

Data for outline are provided by method .get_outlineexplorer_data() of
highlighter of assigned editor. For example, for Python files code editor uses
highlighter trex.utils.syntaxhighlighters.PythonSH
"""

# Third party imports
from qtpy.QtCore import Signal

# Local imports
from trex.config.base import _
from trex.plugins import TRexPluginMixin
from trex.py3compat import is_text_string
from trex.utils import icon_manager as ima
from trex.widgets.editortools import OutlineExplorerWidget


class OutlineExplorer(OutlineExplorerWidget, TRexPluginMixin):
    CONF_SECTION = 'outline_explorer'
    sig_option_changed = Signal(str, object)
    
    def __init__(self, parent=None, fullpath_sorting=True):
        show_fullpath = self.get_option('show_fullpath')
        show_all_files = self.get_option('show_all_files')
        show_comments = self.get_option('show_comments')
        OutlineExplorerWidget.__init__(self, parent=parent,
                                       show_fullpath=show_fullpath,
                                       fullpath_sorting=fullpath_sorting,
                                       show_all_files=show_all_files,
                                       show_comments=show_comments)
        TRexPluginMixin.__init__(self, parent)

        # Initialize plugin
        self.initialize_plugin()
        
        self.treewidget.header().hide()
        self.load_config()
        
    #------ TRexPluginWidget API ---------------------------------------------    
    def get_plugin_title(self):
        """Return widget title"""
        return _("Outline")

    def get_plugin_icon(self):
        """Return widget icon"""
        return ima.icon('outline_explorer')
    
    def get_focus_widget(self):
        """
        Return the widget to give focus to when
        this plugin's dockwidget is raised on top-level
        """
        return self.treewidget
    
    def get_plugin_actions(self):
        """Return a list of actions related to plugin"""
        return []
    
    def register_plugin(self):
        """Register plugin in TRex's main window"""
        self.main.restore_scrollbar_position.connect(
                                               self.restore_scrollbar_position)
        self.main.add_dockwidget(self)
        
    def refresh_plugin(self):
        """Refresh project explorer widget"""
        pass
        
    def closing_plugin(self, cancelable=False):
        """Perform actions before parent main window is closed"""
        self.save_config()
        return True

    #------ TRexPluginMixin API ---------------------------------------------
    def visibility_changed(self, enable):
        """DockWidget visibility has changed"""
        TRexPluginMixin.visibility_changed(self, enable)
        if enable:
            self.outlineexplorer_is_visible.emit()
            
    #------ Public API ---------------------------------------------------------
    def restore_scrollbar_position(self):
        """Restoring scrollbar position after main window is visible"""
        scrollbar_pos = self.get_option('scrollbar_position', None)
        if scrollbar_pos is not None:
            self.treewidget.set_scrollbar_position(scrollbar_pos)

    def save_config(self):
        """Save configuration: tree widget state"""
        for option, value in list(self.get_options().items()):
            self.set_option(option, value)
        self.set_option('expanded_state', self.treewidget.get_expanded_state())
        self.set_option('scrollbar_position',
                        self.treewidget.get_scrollbar_position())
        
    def load_config(self):
        """Load configuration: tree widget state"""
        expanded_state = self.get_option('expanded_state', None)
        # Sometimes the expanded state option may be truncated in .ini file
        # (for an unknown reason), in this case it would be converted to a
        # string by 'userconfig':
        if is_text_string(expanded_state):
            expanded_state = None
        if expanded_state is not None:
            self.treewidget.set_expanded_state(expanded_state)
