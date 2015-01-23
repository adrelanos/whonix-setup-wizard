#!/usr/bin/python
# -*- coding: utf-8 -*-

""" WHONIX SETUP WIZARD """
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from PyQt4 import QtCore, QtGui
#from PyQt4.QtGui import *
from subprocess import call
import os, yaml
import inspect
import sys
#from PyQt4.QtCore import Qt
#from PyQt4.QtGui import QApplication, QCursor

from guimessages.translations import _translations
from guimessages.guimessage import gui_message

import tor_status


class common:
    """ Variables and constants used through all the classes
    """
    translations_path ='/usr/share/translations/whonix_setup.yaml'

    is_complete = False

    run_repo = False
    disable_repo = False

    tor_status = ''

    argument = sys.argv[1]

    if argument == 'setup':
        if os.path.exists('/usr/share/anon-gw-base-files'):
            environment = 'gateway'
            wizard_steps = ['disclaimer_1',
                            'disclaimer_2',
                            'connection_page',
                            'tor_status_page',
                            'whonix_repo_page',
                            'repository_wizard_page_1',
                            'repository_wizard_page_2',
                            'repository_wizard_finish',
                            'finish_page',
                            'first_use_notice']

        elif os.path.exists('/usr/share/anon-ws-base-files'):
            environment = 'workstation'
            wizard_steps = ['disclaimer_1',
                            'disclaimer_2',
                            'whonix_repo_page',
                            'repository_wizard_page_1',
                            'repository_wizard_page_2',
                            'repository_wizard_finish',
                            'finish_page']

    elif argument == 'repository':
        wizard_steps = ['repository_wizard_page_1',
                        'repository_wizard_page_2',
                        'repository_wizard_finish']

    elif argument == 'locale_settings':
        wizard_steps = ['locale_settings',
                        'locale_settings_finish']

    first_use_notice = False

    if environment == 'gateway':
        if not os.path.exists("/home/user/.gateway/first_use_check.done"):
            first_use_notice = True
        else:
            first_use_notice = False



class locale_settings(QtGui.QWizardPage):
    def __init__(self):
        super(locale_settings, self).__init__()

        self.text = QtGui.QLabel(self)

        self.group = QtGui.QGroupBox(self)

        self.default_button = QtGui.QRadioButton(self.group)
        self.other_button = QtGui.QRadioButton(self.group)

        self.lang_checkbox = QtGui.QCheckBox(self.group)
        self.kbd_checkbox = QtGui.QCheckBox(self.group)

        self.layout = QtGui.QVBoxLayout(self)

        self.setup_ui()

    def setup_ui(self):
        self.text.setMaximumSize(QtCore.QSize(400, 24))
        self.text.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.text.setText('Whonix installation language.')

        self.group.setMinimumSize(0, 112)

        self.default_button.setGeometry(QtCore.QRect(20, 16, 483, 21))
        self.default_button.setText('Default (English (US)')
        self.default_button.setChecked(True)

        self.other_button.setGeometry(QtCore.QRect(20, 36, 483, 21))
        self.other_button.setText('Other')
        self.other_button.toggled.connect(self.other_button_toggled)

        self.lang_checkbox.setEnabled(False)
        self.lang_checkbox.setChecked(True)
        self.lang_checkbox.setGeometry(QtCore.QRect(40, 58, 483, 21))
        self.lang_checkbox.setText('Change country and language')
        self.lang_checkbox.toggled.connect(self.lang_checkbox_toggled)

        self.kbd_checkbox.setEnabled(False)
        self.kbd_checkbox.setChecked(True)
        self.kbd_checkbox.setGeometry(QtCore.QRect(40, 78, 483, 21))
        self.kbd_checkbox.setText('Change keyboard layout')
        self.kbd_checkbox.toggled.connect(self.kbd_checkbox_toggled)

        self.layout.addWidget(self.text)
        self.layout.addWidget(self.group)

        self.setLayout(self.layout)

    def other_button_toggled(self, state):
        if state:
            self.lang_checkbox.setEnabled(True)
            self.kbd_checkbox.setEnabled(True)

        else:
            self.lang_checkbox.setEnabled(False)
            self.kbd_checkbox.setEnabled(False)

    def lang_checkbox_toggled(self, state):
        if (not self.lang_checkbox.isChecked() and
            not self.kbd_checkbox.isChecked()):
            self.lang_checkbox.setChecked(True)
            self.kbd_checkbox.setChecked(True)
            self.default_button.setChecked(True)
            self.other_button.setChecked(False)

    def kbd_checkbox_toggled(self, state):
        if (not self.lang_checkbox.isChecked() and
            not self.kbd_checkbox.isChecked()):
            self.lang_checkbox.setChecked(True)
            self.kbd_checkbox.setChecked(True)
            self.default_button.setChecked(True)
            self.other_button.setChecked(False)


class locale_settings_finish(QtGui.QWizardPage):
    def __init__(self):
        super(locale_settings_finish, self).__init__()

        self.text = QtGui.QTextBrowser(self)
        self.layout = QtGui.QVBoxLayout()

        self.setup_ui()

    def setup_ui(self):
        self.text.setFrameShape(QtGui.QFrame.NoFrame)
        self.layout.addWidget(self.text)

        self.setLayout(self.layout)


class disclaimer_page_1(QtGui.QWizardPage):
    def __init__(self):
        super(disclaimer_page_1, self).__init__()

        self.steps = common.wizard_steps

        self.text = QtGui.QTextBrowser(self)
        self.accept_group = QtGui.QGroupBox(self)
        self.yes_button = QtGui.QRadioButton(self.accept_group)
        self.no_button = QtGui.QRadioButton(self.accept_group)

        self.layout = QtGui.QVBoxLayout()

        self.setupUi()

    def setupUi(self):
        self.text.setFrameShape(QtGui.QFrame.Panel)
        self.text.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)

        self.accept_group.setMinimumSize(0, 60)
        self.yes_button.setGeometry(QtCore.QRect(30, 10, 300, 21))
        self.no_button.setGeometry(QtCore.QRect(30, 30, 300, 21))
        self.no_button.setChecked(True)

        self.layout.addWidget(self.text)
        self.layout.addWidget(self.accept_group)
        self.setLayout(self.layout)

    def nextId(self):
        if self.yes_button.isChecked():
            return self.steps.index('disclaimer_2')
        # Not understood
        elif self.no_button.isChecked():
            return self.steps.index('finish_page')


class disclaimer_page_2(QtGui.QWizardPage):
    def __init__(self):
        super(disclaimer_page_2, self).__init__()

        self.steps = common.wizard_steps
        self.env = common.environment

        self.text = QtGui.QTextBrowser(self)
        self.accept_group = QtGui.QGroupBox(self)
        self.yes_button = QtGui.QRadioButton(self.accept_group)
        self.no_button = QtGui.QRadioButton(self.accept_group)

        self.layout = QtGui.QVBoxLayout()

        self.setupUi()

    def setupUi(self):
        self.text.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.text.setFrameShape(QtGui.QFrame.Panel)

        self.accept_group.setMinimumSize(0, 60)
        self.yes_button.setGeometry(QtCore.QRect(30, 10, 300, 21))
        self.no_button.setGeometry(QtCore.QRect(30, 30, 300, 21))
        self.no_button.setChecked(True)

        self.layout.addWidget(self.text)
        self.layout.addWidget(self.accept_group)
        self.setLayout(self.layout)

    def nextId(self):
        if self.yes_button.isChecked():
            if not os.path.exists('/var/lib/whonix/do_once/whonixsetup.done'):
                common.run_repo = True
                if self.env == 'gateway':
                    return self.steps.index('connection_page')
                elif self.env == 'workstation':
                # run whonix_repository_wizard
                    return self.steps.index('whonix_repo_page')
            else:
                if self.env == 'gateway':
                    return self.steps.index('connection_page')
                elif self.env == 'workstation':
                    return self.steps.index('finish_page')
        # Not understood
        else:
            return self.steps.index('finish_page')


class connection_page(QtGui.QWizardPage):
    def __init__(self):
        super(connection_page, self).__init__()

        translation = _translations(common.translations_path, 'whonixsetup')
        self._ = translation.gettext

        self.common = common()
        self.steps = self.common.wizard_steps
        self.env = self.common.environment

        self.text = QtGui.QTextBrowser(self)
        self.layout = QtGui.QGridLayout()

        self.connection_group = QtGui.QGroupBox(self)
        self.enable = QtGui.QRadioButton(self.connection_group)
        self.disable = QtGui.QRadioButton(self.connection_group)
        self.censored = QtGui.QRadioButton(self.connection_group)
        self.use_proxy = QtGui.QRadioButton(self.connection_group)

        self.layout = QtGui.QVBoxLayout()

        self.setupUi()

    def setupUi(self):
        self.text.setFrameShape(QtGui.QFrame.NoFrame)
        self.text.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)

        self.connection_group.setMinimumSize(0, 100)

        self.enable.setGeometry(QtCore.QRect(30, 10, 400, 21))
        self.enable.setToolTip(self._('tooltip_1'))

        self.disable.setGeometry(QtCore.QRect(30, 30, 400, 21))
        self.disable.setToolTip(self._('tooltip_2'))

        self.censored.setGeometry(QtCore.QRect(30, 50, 400, 21))
        self.censored.setToolTip(self._('tooltip_3'))

        self.use_proxy.setGeometry(QtCore.QRect(30, 70, 400, 21))
        self.use_proxy.setToolTip(self._('tooltip_4'))

        self.enable.setChecked(True)

        self.layout.addWidget(self.text)
        self.layout.addWidget(self.connection_group)
        self.setLayout(self.layout)


class tor_status_page(QtGui.QWizardPage):
    def __init__(self):
        super(tor_status_page, self).__init__()

        self.steps = common.wizard_steps

        self.icon = QtGui.QLabel(self)
        self.text = QtGui.QTextBrowser(self)
        self.torrc = QtGui.QPlainTextEdit(self)

        self.layout = QtGui.QGridLayout()
        self.setupUi()

    def setupUi(self):
        self.icon.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.icon.setMinimumSize(50, 0)

        self.text.setFrameShape(QtGui.QFrame.NoFrame)
        self.text.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)

        self.torrc.setMinimumSize(0, 185)
        self.torrc.setReadOnly(True)

        self.layout.addWidget(self.icon, 0, 0, 1, 1)
        self.layout.addWidget(self.text, 0, 1, 1, 2)
        self.layout.addWidget(self.torrc, 1, 1, 1, 1)
        self.setLayout(self.layout)

    def nextId(self):
        if common.run_repo:
            return self.steps.index('whonix_repo_page')
        else:
            return self.steps.index('finish_page')


class whonix_repository_page(QtGui.QWizardPage):
    def __init__(self):
        super(whonix_repository_page, self).__init__()

        self.steps = common.wizard_steps

        self.text = QtGui.QTextBrowser(self)
        self.layout = QtGui.QGridLayout()

        self.setupUi()

    def setupUi(self):
        self.text.setFrameShape(QtGui.QFrame.NoFrame)
        self.text.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)

        self.layout.addWidget(self.text)
        self.setLayout(self.layout)

    def nextId(self):
        common.run_repo = True
        return self.steps.index('repository_wizard_page_1')


class repository_wizard_page_1(QtGui.QWizardPage):
    def __init__(self):
        super(repository_wizard_page_1, self).__init__()

        self.steps = common.wizard_steps

        self.text = QtGui.QTextBrowser(self)

        self.enable_group = QtGui.QGroupBox(self)
        self.enable_repo = QtGui.QRadioButton(self.enable_group)
        self.disable_repo = QtGui.QRadioButton(self.enable_group)

        self.layout = QtGui.QVBoxLayout()

        self.setupUi()

    def setupUi(self):
        self.text.setFrameShape(QtGui.QFrame.NoFrame)
        self.text.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.text.setOpenExternalLinks(True)

        self.enable_group.setMinimumSize(0, 60)
        self.enable_repo.setGeometry(QtCore.QRect(30, 10, 400, 21))
        self.disable_repo.setGeometry(QtCore.QRect(30, 30, 400, 21))

        self.enable_repo.setChecked(True)

        self.layout.addWidget(self.text)
        self.layout.addWidget(self.enable_group)
        self.setLayout(self.layout)

    def nextId(self):
        if self.enable_repo.isChecked():
            return self.steps.index('repository_wizard_page_2')

        elif self.disable_repo.isChecked():
            common.disable_repo = True
            return self.steps.index('repository_wizard_finish')


class repository_wizard_page_2(QtGui.QWizardPage):
    def __init__(self):
        super(repository_wizard_page_2, self).__init__()

        self.text = QtGui.QTextBrowser(self)

        self.repo_group = QtGui.QGroupBox(self)
        self.stable_repo = QtGui.QRadioButton(self.repo_group)
        self.testers_repo = QtGui.QRadioButton(self.repo_group)
        self.devs_repo = QtGui.QRadioButton(self.repo_group)

        self.layout = QtGui.QVBoxLayout()

        self.setupUi()

    def setupUi(self):
        self.text.setFrameShape(QtGui.QFrame.NoFrame)
        self.text.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)

        self.repo_group.setMinimumSize(0, 80)
        self.stable_repo.setGeometry(QtCore.QRect(30, 10, 400, 21))
        self.testers_repo.setGeometry(QtCore.QRect(30, 30, 400, 21))
        self.devs_repo.setGeometry(QtCore.QRect(30, 50, 400, 21))

        self.stable_repo.setText("Whonix Stable Repository")
        self.testers_repo.setText("Whonix Testers Repository")
        self.devs_repo.setText("Whonix Developers Repository")

        self.stable_repo.setChecked(True)

        self.layout.addWidget(self.text)
        self.layout.addWidget(self.repo_group)
        self.setLayout(self.layout)


class repository_wizard_finish(QtGui.QWizardPage):
    def __init__(self):
        super(repository_wizard_finish, self).__init__()

        self.text = QtGui.QTextBrowser(self)
        self.layout = QtGui.QVBoxLayout()

        self.setupUi()

    def setupUi(self):
        self.text.setFrameShape(QtGui.QFrame.NoFrame)
        self.text.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)

        self.layout.addWidget(self.text)
        self.setLayout(self.layout)


class finish_page(QtGui.QWizardPage):
    def __init__(self):
        super(finish_page, self).__init__()

        self.icon = QtGui.QLabel(self)
        self.text = QtGui.QTextBrowser(self)

        self.layout = QtGui.QGridLayout()
        self.setupUi()

    def setupUi(self):
        self.icon.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.icon.setMinimumSize(50, 0)

        self.text.setFrameShape(QtGui.QFrame.NoFrame)
        self.text.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)

        self.layout.addWidget(self.icon, 0, 0, 1, 1)
        self.layout.addWidget(self.text, 0, 1, 1, 1)
        self.setLayout(self.layout)


class first_use_notice(QtGui.QWizardPage):
    def __init__(self):
        super(first_use_notice, self).__init__()

        self.text = QtGui.QTextBrowser(self)

        self.layout = QtGui.QVBoxLayout()
        self.setupUi()

    def setupUi(self):
        self.text.setFrameShape(QtGui.QFrame.NoFrame)
        self.text.setAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)

        self.layout.addWidget(self.text)
        self.setLayout(self.layout)


class whonix_setup_wizard(QtGui.QWizard):
    def __init__(self):
        super(whonix_setup_wizard, self).__init__()

        translation = _translations(common.translations_path, 'whonixsetup')
        self._ = translation.gettext

        self.steps = common.wizard_steps

        if common.argument == 'repository':
            self.repository_wizard_page_1 = repository_wizard_page_1()
            self.addPage(self.repository_wizard_page_1)

            self.repository_wizard_page_2 = repository_wizard_page_2()
            self.addPage(self.repository_wizard_page_2)

            self.repository_wizard_finish = repository_wizard_finish()
            self.addPage(self.repository_wizard_finish)

        elif common.argument == 'setup':
            self.env = common.environment

            self.disclaimer_1 = disclaimer_page_1()
            self.addPage(self.disclaimer_1)

            self.disclaimer_2 = disclaimer_page_2()
            self.addPage(self.disclaimer_2)

            if self.env == 'gateway':
                self.connection_page = connection_page()
                self.addPage(self.connection_page)

                self.tor_status_page = tor_status_page()
                self.addPage(self.tor_status_page)

            self.whonix_repo_page = whonix_repository_page()
            self.addPage(self.whonix_repo_page)

            self.repository_wizard_page_1 = repository_wizard_page_1()
            self.addPage(self.repository_wizard_page_1)

            self.repository_wizard_page_2 = repository_wizard_page_2()
            self.addPage(self.repository_wizard_page_2)

            self.repository_wizard_finish = repository_wizard_finish()
            self.addPage(self.repository_wizard_finish)

            self.finish_page = finish_page()
            self.addPage(self.finish_page)

            if self.env == 'gateway'and common.first_use_notice:
                self.first_use_notice = first_use_notice()
                self.addPage(self.first_use_notice)

        elif common.argument == 'locale_settings':
            self.locale_settings = locale_settings()
            self.addPage(self.locale_settings)

            self.locale_settings_finish = locale_settings_finish()
            self.addPage(self.locale_settings_finish)

        self.setupUi()

    def setupUi(self):
        self.setWindowIcon(QtGui.QIcon("/usr/share/icons/anon-icon-pack/whonix.ico"))
        self.setWindowTitle('Whonix Setup Wizard')

        if common.argument == 'setup':
            self.resize(760, 750)
        elif common.argument == 'repository':
            self.resize(580, 370)
        elif common.argument == 'locale_settings':
            self.resize(440, 168)

        # We use QTextBrowser with a white background.
        # Set a default (transparent) background.
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 255, 255, 0))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Base, brush)
        brush = QtGui.QBrush(QtGui.QColor(244, 244, 244))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Base, brush)
        self.setPalette(palette)

        try:
            if common.argument == 'setup':
                self.disclaimer_1.text.setText(self._('disclaimer_1'))
                self.disclaimer_1.yes_button.setText(self._('accept'))
                self.disclaimer_1.no_button.setText(self._('reject'))

                self.disclaimer_2.text.setText(self._('disclaimer_2'))
                self.disclaimer_2.yes_button.setText(self._('accept'))
                self.disclaimer_2.no_button.setText(self._('reject'))

                if self.env == 'gateway':
                    self.connection_page.text.setText(self._('connection_text'))
                    self.connection_page.enable.setText(self._('enable_tor'))
                    self.connection_page.disable.setText(self._('disable_tor'))
                    self.connection_page.censored.setText(self._('censored_tor'))
                    self.connection_page.use_proxy.setText(self._('use_proxy'))

                    if common.first_use_notice:
                        self.first_use_notice.text.setText(self._('first_use_notice'))


            if common.argument == 'setup' or common.argument == 'repository':
                self.repository_wizard_page_1.text.setText(self._('repo_page_1'))
                self.repository_wizard_page_1.enable_repo.setText(self._('repo_enable'))
                self.repository_wizard_page_1.disable_repo.setText(self._('repo_disable'))

                self.repository_wizard_page_2.text.setText(self._('repo_page_2'))

        except (yaml.scanner.ScannerError, yaml.parser.ParserError):
            pass

        #self.setOption(QtGui.QWizard.HaveHelpButton, True)
        self.button(QtGui.QWizard.CancelButton).setVisible(False)

        self.button(QtGui.QWizard.BackButton).clicked.connect(self.BackButton_clicked)
        self.button(QtGui.QWizard.NextButton).clicked.connect(self.NextButton_clicked)

        # Temporary workaround.
        # The pluggable transports are not implemented yet, but we want to
        # be able to display the tooltips for censored and firewall. For this,
        # the options must be enabled, but the slot will disable the Next
        # button if either is checked.
        if common.argument == 'setup':
            if self.env == 'gateway':
                self.connection_page.censored.toggled.connect(self.set_next_button_state)
                self.connection_page.use_proxy.toggled.connect(self.set_next_button_state)

        self.exec_()

    # called by button toggled signal.
    def set_next_button_state(self, state):
        if state:
            self.button(QtGui.QWizard.NextButton).setEnabled(False)
        else:
            self.button(QtGui.QWizard.NextButton).setEnabled(True)

    def center(self):
        """ After the window is resized, its origin point becomes the
        previous window top left corner.
        Re-center the window on the screen.
        """
        frame_gm = self.frameGeometry()
        center_point = QtGui.QDesktopWidget().availableGeometry().center()
        frame_gm.moveCenter(center_point)
        self.move(frame_gm.topLeft())

    def NextButton_clicked(self):
        """ Next button slot.
        The commands cannot be implemented in the wizard's nextId() function,
        as it is polled by the event handler on the creation of the page.
        Depending on the checkbox states, the commands would be run when the
        page is loaded.
        Those button_clicked functions are called once, when the user clicks
        the corresponding button.
        Options (like button states, window size changes...) are set here.
        """
        if common.argument == 'setup':

            if self.env == 'workstation':
                if (self.currentId() == self.steps.index('whonix_repo_page') or
                    self.currentId() == self.steps.index('finish_page')):
                    self.resize(470, 310)
                    self.center()

            if self.env == 'gateway':
                if self.currentId() == self.steps.index('connection_page'):
                    self.resize(580, 370)
                    self.center()

                # Set Next button state
                if self.currentId() == self.steps.index('connection_page'):
                    if (self.connection_page.censored.isChecked() or
                        self.connection_page.use_proxy.isChecked()):
                            self.button(QtGui.QWizard.NextButton).setEnabled(False)
                    else:
                            self.button(QtGui.QWizard.NextButton).setEnabled(True)

                if self.currentId() == self.steps.index('tor_status_page'):
                    if self.connection_page.enable.isChecked():

                        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
                        common.tor_status = tor_status.set_enabled()
                        QApplication.restoreOverrideCursor()

                        if common.tor_status == 'tor_enabled':
                            self.tor_status_page.text.setText(self._('tor_enabled'))
                            torrc_text = open('/etc/tor/torrc').read()
                            self.tor_status_page.torrc.setPlainText(torrc_text)
                            self.tor_status_page.icon.setPixmap(QtGui.QPixmap( \
                                '/usr/share/icons/oxygen/48x48/status/task-complete.png'))

                        elif common.tor_status == 'tor_already_enabled':
                            self.tor_status_page.text.setText(self._('tor_already_enabled'))
                            torrc_text = open('/etc/tor/torrc').read()
                            self.tor_status_page.torrc.setPlainText(torrc_text)
                            self.tor_status_page.icon.setPixmap(QtGui.QPixmap( \
                                '/usr/share/icons/oxygen/48x48/status/task-complete.png'))

                        else:
                            self.tor_status_page.torrc.setFrameShape(QtGui.QFrame.NoFrame)
                            self.tor_status_page.text.setText(self._('something_wrong'))
                            self.tor_status_page.icon.setPixmap(QtGui.QPixmap( \
                                '/usr/share/icons/oxygen/48x48/status/task-reject.png'))
                            common.run_repo = False
                            # Do not run whonixrepository
                            self.removePage(self.steps.index('whonix_repo_page'))
                            self.removePage(self.steps.index('repository_wizard_page_1'))
                            self.removePage(self.steps.index('repository_wizard_page_2'))
                            self.removePage(self.steps.index('repository_wizard_finish'))

                    elif self.connection_page.disable.isChecked():

                        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
                        common.tor_status = tor_status.set_disabled()
                        QApplication.restoreOverrideCursor()

                        if common.tor_status == 'tor_disabled':
                            self.tor_status_page.text.setText(self._('tor_disabled'))
                            torrc_text = open('/etc/tor/torrc').read()
                            self.tor_status_page.torrc.setPlainText(torrc_text)
                            self.tor_status_page.icon.setPixmap(QtGui.QPixmap( \
                                '/usr/share/icons/oxygen/48x48/status/task-attention.png'))

                        elif common.tor_status == 'tor_already_disabled':
                            self.tor_status_page.text.setText(self._('tor_already_disabled'))
                            torrc_text = open('/etc/tor/torrc').read()
                            self.tor_status_page.torrc.setPlainText(torrc_text)
                            self.tor_status_page.icon.setPixmap(QtGui.QPixmap( \
                                '/usr/share/icons/oxygen/48x48/status/task-attention.png'))

                        else:
                            self.tor_status_page.torrc.setFrameShape(QtGui.QFrame.NoFrame)
                            self.tor_status_page.text.setText(self._('something_wrong'))
                            self.tor_status_page.icon.setPixmap(QtGui.QPixmap( \
                                '/usr/share/icons/oxygen/48x48/status/task-reject.png'))
                            # Do not run whonixrepository
                            common.run_repo = False
                            self.removePage(self.steps.index('whonix_repo_page'))
                            self.removePage(self.steps.index('repository_wizard_page_1'))
                            self.removePage(self.steps.index('repository_wizard_page_2'))
                            self.removePage(self.steps.index('repository_wizard_finish'))

            if self.currentId() == self.steps.index('whonix_repo_page'):
                if os.path.exists('/usr/bin/whonix-repository-wizard'):
                    self.whonix_repo_page.text.setText(self._('whonix_repository_page'))

                else:
                    common.run_repo = False
                    self.whonix_repo_page.text.setText(self._('repository_wizard_not_found'))

        if common.argument == 'setup' or common.argument == 'repository':
            if self.currentId() == self.steps.index('repository_wizard_finish'):
                if common.disable_repo:
                    command = 'whonix_repository --disable'

                    QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
                    exit_code = call(command, shell=True)
                    QApplication.restoreOverrideCursor()

                    mypath = inspect.getfile(inspect.currentframe())

                    if exit_code == 0:
                        self.repository_wizard_finish.text.setText(self._('repo_finish_disabled'))
                        message = 'INFO %s: Ok, exit code of "%s" was %s.' % ( mypath, command, exit_code )

                    else:
                        error = '<p>ERROR %s: exit code of \"%s\" was %s.</p>' % ( mypath, command, exit_code )
                        finish_text_failed =  error + self.finish_text_failed
                        self.repository_wizard_finish.text.setText(self._('repo_finish_failed'))
                        message = error

                    command = 'echo ' + message
                    call(command, shell=True)
                    self.one_shot = False

                else:
                    if self.repository_wizard_page_2.stable_repo.isChecked():
                        codename = ' --codename stable'

                    elif self.repository_wizard_page_2.testers_repo.isChecked():
                        codename = ' --codename testers'

                    elif self.repository_wizard_page_2.devs_repo.isChecked():
                        codename = ' --codename developers'

                    command = 'whonix_repository --enable' + codename

                    QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
                    exit_code = call(command, shell=True)
                    QApplication.restoreOverrideCursor()

                    mypath = inspect.getfile(inspect.currentframe())

                    if exit_code == 0:
                        self.repository_wizard_finish.text.setText(self._('repo_finish_enabled'))
                        message = 'INFO %s: Ok, exit code of "%s" was %s.' % ( mypath, command, exit_code )

                    else:
                        error = '<p>ERROR %s: exit code of \"%s\" was %s.</p>' % ( mypath, command, exit_code )
                        finish_text_failed =  error + self.finish_text_failed
                        self.repository_wizard_finish.text.setText(self._('repo_finish_failed'))
                        message = error

                    command = 'echo ' + message
                    call(command, shell=True)
                    self.one_shot = False

        if common.argument == 'setup':
            if self.currentId() == self.steps.index('finish_page'):
                # for whonixcheck.
                common.is_complete = True

                if common.run_repo:
                    #  Do not run whonix-repository-wizard twice.
                    common.run_repo = False
                    self.removePage(self.steps.index('whonix_repo_page'))
                    self.removePage(self.steps.index('repository_wizard_page_1'))
                    self.removePage(self.steps.index('repository_wizard_page_2'))
                    self.removePage(self.steps.index('repository_wizard_finish'))

                if self.env == 'workstation':
                    self.finish_page.icon.setPixmap(QtGui.QPixmap( \
                        '/usr/share/icons/oxygen/48x48/status/task-complete.png'))
                    self.finish_page.text.setText(self._('finish_page_ok'))

                if self.env == 'gateway':
                    if (common.tor_status == 'tor_enabled' or
                        common.tor_status == 'tor_already_enabled'):
                            self.finish_page.icon.setPixmap(QtGui.QPixmap( \
                                '/usr/share/icons/oxygen/48x48/status/task-complete.png'))
                            self.finish_page.text.setText(self._('finish_page_ok'))

                            # whonixsetup completed.
                            if not os.path.exists('/var/lib/whonix/do_once'):
                                os.mkdir('/var/lib/whonix/do_once')

                            whonixsetup_done = open('/var/lib/whonix/do_once/whonixsetup.done', 'w')
                            whonixsetup_done.close()

                    else:
                        common.is_complete = False

                        if (common.tor_status == 'tor_disabled' or
                            common.tor_status == 'tor_already_disabled'):
                            self.finish_page.icon.setPixmap(QtGui.QPixmap( \
                                '/usr/share/icons/oxygen/48x48/status/task-attention.png'))
                            self.finish_page.text.setText(self._('finish_disabled'))

                        # ERROR pages.
                        elif common.tor_status == 'no_torrc':
                            self.finish_page.icon.setPixmap(QtGui.QPixmap( \
                                '/usr/share/icons/oxygen/48x48/status/task-reject.png'))
                            self.button(QtGui.QWizard.BackButton).setEnabled(False)
                            self.finish_page.text.setText(self._('no_torrc'))

                        elif common.tor_status == 'bad_torrc':
                            self.finish_page.icon.setPixmap(QtGui.QPixmap( \
                                '/usr/share/icons/oxygen/48x48/status/task-reject.png'))
                            self.button(QtGui.QWizard.BackButton).setEnabled(False)
                            self.finish_page.text.setText(self._('bad_torrc'))

                        elif common.tor_status == 'cannot_connect':
                            # #DisableNetwork 0 was uncommented. re-comment.
                            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
                            common.tor_status = tor_status.set_disabled()
                            QApplication.restoreOverrideCursor()

                            self.finish_page.icon.setPixmap(QtGui.QPixmap( \
                                '/usr/share/icons/oxygen/48x48/status/task-reject.png'))
                            self.button(QtGui.QWizard.BackButton).setEnabled(False)
                            self.finish_page.text.setText(self._('cannot_connect'))

                # Disclaimer page 1 not undesrstood -> leave
                if self.disclaimer_1.no_button.isChecked():
                    self.hide()
                    command = '/sbin/poweroff'
                    call(command, shell=True)

                # Disclaimer page 2 not undesrstood -> leave
                if self.disclaimer_2.no_button.isChecked():
                    self.hide()
                    command = '/sbin/poweroff'
                    call(command, shell=True)

                if self.env == 'workstation':
                    self.finish_page.text.setText(self._('finish_page_ok'))

                    # whonixsetup completed.
                    if not os.path.exists('/var/lib/whonix/do_once'):
                        os.mkdir('/var/lib/whonix/do_once')

                    whonixsetup_done = open('/var/lib/whonix/do_once/whonixsetup.done', 'w')
                    whonixsetup_done.close()

        if common.argument == 'locale_settings':
            if self.currentId() == self.steps.index('locale_settings_finish'):

                if self.locale_settings.other_button.isChecked():

                    if self.locale_settings.lang_checkbox.isChecked():
                        command = '/usr/bin/kcmshell4 language'
                        call(command, shell=True)

                    if self.locale_settings.kbd_checkbox.isChecked():
                        command = '/usr/bin/kcmshell4 kcm_keyboard'
                        call(command, shell=True)

                    self.button(QtGui.QWizard.BackButton).setEnabled(False)
                    self.locale_settings_finish.text.setText(self._('locale_notice'))

                else:
                    text = ('<p>Whonix will be installed in the default language (English US).</p> \
                            Click "Finish" to start the deskop environment')
                    self.locale_settings_finish.text.setText(text)

    def BackButton_clicked(self):
        common.is_complete = False

        if common.argument == 'setup':
            if self.currentId() == self.steps.index('disclaimer_2'):
                # Back to disclaimer size.
                self.resize(760, 750)
                self.center()


def main():
    #import sys
    app = QtGui.QApplication(sys.argv)

    if not os.path.exists('/usr/bin/kcmshell4'):
        sys.exit(0)

    # root check.
    # locale_settings has to be run as user.
    if sys.argv[1] != 'locale_settings':
        if os.getuid() != 0:
            print 'ERROR: This must be run as root!\nUse "kdesudo".'
            not_root = gui_message(common.translations_path, 'not_root')
            sys.exit(1)

    wizard = whonix_setup_wizard()

    if common.first_use_notice:
        f = open("/home/user/.gateway/first_use_check.done", "w")
        f.close()

    # run whonixcheck
    if common.is_complete:
        command = '/usr/lib/whonixsetup_/ft_m_end'
        call(command, shell=True)

    sys.exit()

if __name__ == "__main__":
    main()
