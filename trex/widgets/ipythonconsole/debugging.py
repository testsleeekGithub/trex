# -*- coding: utf-8 -*-
#
# Copyright © TRex Project Contributors
# Licensed under the terms of the MIT License
# (see trex/__init__.py for details)

"""
Widget that handles communications between a console in debugging
mode and TRex
"""

import ast

from qtpy.QtCore import QEventLoop

from qtconsole.rich_jupyter_widget import RichJupyterWidget

from trex.py3compat import to_text_string


class DebuggingWidget(RichJupyterWidget):
    """
    Widget with the necessary attributes and methods to handle
    communications between a console in debugging mode and
    TRex
    """

    _input_reply = {}
    _input_reply_failed = False

    # --- Public API --------------------------------------------------
    def silent_exec_input(self, code):
        """Silently execute code through stdin"""
        self._hidden = True

        # Wait until the kernel returns an answer
        wait_loop = QEventLoop()
        self.sig_input_reply.connect(wait_loop.quit)
        self.kernel_client.iopub_channel.flush()
        self.kernel_client.input(code)
        wait_loop.exec_()

        # Remove loop connection and loop
        self.sig_input_reply.disconnect(wait_loop.quit)
        wait_loop = None

        # Restore hidden state
        self._hidden = False

        # Emit signal
        if isinstance(self._input_reply, dict):
            if 'pdb_step' in code and 'fname' in self._input_reply:
                fname = self._input_reply['fname']
                lineno = self._input_reply['lineno']
                self.sig_pdb_step.emit(fname, lineno)
            elif 'get_namespace_view' in code:
                if 'fname' not in self._input_reply:
                    view = self._input_reply
                else:
                    view = None
                self.sig_namespace_view.emit(view)
            elif 'get_var_properties' in code:
                if 'fname' not in self._input_reply:
                    properties = self._input_reply
                else:
                    properties = None
                self.sig_var_properties.emit(properties)
        else:
            self.kernel_client.iopub_channel.flush()
            self._input_reply = {}
            self._input_reply_failed = True
            self.sig_dbg_kernel_restart.emit()

    def write_to_stdin(self, line):
        """Send raw characters to the IPython kernel through stdin"""
        wait_loop = QEventLoop()
        self.kernel_client.iopub_channel.flush()
        self.sig_prompt_ready.connect(wait_loop.quit)
        self.kernel_client.input(line)
        wait_loop.exec_()

        # Remove loop connection and loop
        self.sig_prompt_ready.disconnect(wait_loop.quit)
        wait_loop = None

        # Run post exec commands
        self._post_exec_input(line)

    def set_trex_breakpoints(self):
        """Set TRex breakpoints into a debugging session"""
        if self._reading:
            self.kernel_client.input(
                "!get_ipython().kernel._set_trex_breakpoints()")

    # ---- Private API (defined by us) -------------------------------
    def _post_exec_input(self, line):
        """Commands to be run after writing to stdin"""
        if self._reading:
            pdb_commands = ['next', 'continue', 'step', 'return']
            if any([x == line for x in pdb_commands]):
                # To open the file where the current pdb frame points to
                self.silent_exec_input("!get_ipython().kernel.get_pdb_step()")

                # To refresh the Variable Explorer
                self.silent_exec_input(
                    "!get_ipython().kernel.get_namespace_view()")
                self.silent_exec_input(
                    "!get_ipython().kernel.get_var_properties()")

    # ---- Private API (overrode by us) -------------------------------
    def _handle_input_request(self, msg):
        """
        Reimplemented to be able to handle requests when we ask for
        hidden inputs
        """
        self.kernel_client.iopub_channel.flush()
        if not self._hidden:
            def callback(line):
                self.kernel_client.input(line)
            if self._reading:
                self._reading = False
            self._readline(msg['content']['prompt'], callback=callback,
                           password=msg['content']['password'])
        else:
            # This is what we added, i.e. not doing anything if
            # TRex asks for silent inputs
            pass

    def _handle_stream(self, msg):
        """
        Reimplemented to handle input replies in hidden mode
        """
        if not self._hidden:
            self.flush_clearoutput()
            self.append_stream(msg['content']['text'])
            # This signal is a clear indication that all stdout
            # has been handled at this point. Then TRex can
            # proceed to request other inputs
            self.sig_prompt_ready.emit()
        else:
            # This allows TRex to receive, transform and save the
            # contents of a silent execution
            content = msg.get('content', '')
            if content:
                name = content.get('name', '')
                if name == 'stdout':
                    text = content['text']
                    text = to_text_string(text.replace('\n', ''))
                    try:
                        reply = ast.literal_eval(text)
                    except:
                        reply = None
                    if not isinstance(reply, dict):
                        self._input_reply = None
                    else:
                        self._input_reply = reply
                    self.sig_input_reply.emit()
                else:
                    self._input_reply = None
                    self.sig_input_reply.emit()
            else:
                self._input_reply = None
                self.sig_input_reply.emit()
