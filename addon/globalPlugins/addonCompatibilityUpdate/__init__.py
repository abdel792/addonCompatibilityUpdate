# -*- coding: utf-8 -*-
# addonCompatibilityUpdate Add-on for NVDA
# Copyright 2022-2023 Abdelkrim Bensaïd, released under gPL.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import globalPluginHandler
import addonHandler
import versionInfo
from . import skipTranslation
import globalVars
import config
import wx
import gui
import core
import os
from scriptHandler import script
from .yearCompatibility import YearCompatibilitySettingsDialog
addonHandler.initTranslation()
confspec = {
	"yearCompatibilityChoice": f"string(default={versionInfo.version_year})",
}
config.conf.spec["addonCompatibilityUpdate"] = confspec

class GlobalPlugin (globalPluginHandler.GlobalPlugin):

	scriptCategory = addonHandler.getCodeAddon().manifest["summary"]

	def __init__(self, *args, **kwargs):
		super(globalPluginHandler.GlobalPlugin, self).__init__(*args, **kwargs)
		if globalVars.appArgs.secure:
			return
		self.toolsMenu = gui.mainFrame.sysTrayIcon.toolsMenu
		self.yearCompatibilitySettings = self.toolsMenu.Append(
			# Translators: The name of the year compatibility item in NVDA Tools menu.
			wx.ID_ANY, _("Change year com&patibility for add-ons..."),
			# Translators: The tooltyp text for the year compatibility item in NVDA Tools menu.
			_("Allows you to choose your year compatibility for your add-ons")
		)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onYearCompatibilitySettingsDialog, self.yearCompatibilitySettings)

	def terminate(self):
		super(GlobalPlugin, self).terminate()
		try:
			self.toolsMenu.Remove(self.yearCompatibilitySettings)
		except (RuntimeError, AttributeError):
			pass

	def onYearCompatibilitySettingsDialog(self, evt):
		try:
			gui.mainFrame.prePopup()
			d = YearCompatibilitySettingsDialog(gui.mainFrame)
			d.Show()
			gui.mainFrame.postPopup()
		except gui.settingsDialogs.SettingsDialog.MultiInstanceErrorWithDialog:
			wx.CallAfter(
				gui.messageBox,
				# Translators: error message when attempting to open more than one year compatibility settings dialogs.
				_("Year compatibility dialog is already open."),
				skipTranslation.translate("Error"), wx.OK | wx.ICON_ERROR
			)

	@script(
		# Translators: Message presented in input help mode.
		description=_("Display the year compatibility settings dialog box.")
	)
	def script_activateYearCompatibilitySettingsDialog(self, gesture):
		wx.CallAfter(self.onYearCompatibilitySettingsDialog, None)


