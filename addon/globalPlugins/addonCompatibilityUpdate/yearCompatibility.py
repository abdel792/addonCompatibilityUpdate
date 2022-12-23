# -*- coding: utf-8 -*-
# addonCompatibilityUpdate Add-on for NVDA
# yearCompatibility.py.
# Copyright 2022-2023 Abdelkrim Bensaïd, released under gPL.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import versionInfo
from . import skipTranslation
import addonHandler
import os
import re
import globalVars
import core
import gui
import config
from gui import SettingsPanel, SettingsDialog
import wx
addonHandler.initTranslation()

def promptUserForRestart():
	restartMessage = skipTranslation.translate(
		# Translators: A message asking the user if they wish to restart NVDA
		# as addons have been added, enabled/disabled or removed.
		"Changes were made to add-ons. "
		"You must restart NVDA for these changes to take effect. "
		"Would you like to restart now?"
	)
	# Translators: Title for message asking if the user wishes to restart NVDA as addons have been added or removed.
	restartTitle = skipTranslation.translate("Restart NVDA")
	result = gui.messageBox(
		message=restartMessage,
		caption=restartTitle,
		style=wx.YES | wx.NO | wx.ICON_WARNING
	)
	if wx.YES == result:
		core.restart()

class YearCompatibilitySettingsDialog(SettingsDialog):

	# Translators: This is the label for the year compatibility settings panel.
	title = _("List of years to choose for add-on compatibility")

	def makeSettings(self, settingsSizer):
		self._yearCompatibilityChoices = tuple([str(x) for x in range (versionInfo.version_year, versionInfo.version_year + 11)])

		# Translators: This is the label for a combo box in the Compatibility year settings dialog.
		self._yearCompatibilityTitle = _("Year compatibility for add-ons:")

		self.showYearCompatibilityDialog(settingsSizer=settingsSizer)

	def postInit(self):
		self._yearCompatibilityChoice.SetFocus()

	def showYearCompatibilityDialog(self, settingsSizer):
		yearCompatibilitySettingsGuiHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		self._yearCompatibilityChoice = yearCompatibilitySettingsGuiHelper.addLabeledControl(
			self._yearCompatibilityTitle, wx.Choice, choices=self._yearCompatibilityChoices
		)

		curChoice = config.conf["addonCompatibilityUpdate"]["yearCompatibilityChoice"]
		for index, name in enumerate(self._yearCompatibilityChoices):
			if name == curChoice:
				self._yearCompatibilityChoice.SetSelection(index)
				break

	def onOk(self, evt):
		super(YearCompatibilitySettingsDialog, self).onOk(evt)
		config.conf["addonCompatibilityUpdate"]["yearCompatibilityChoice"] = self._yearCompatibilityChoice.GetStringSelection()
		match = r"(?<=lastTestedNVDAVersion) ?= ?[0-9\.]+"
		reg = re.compile(match, re.M)
		addonPath = os.path.join(globalVars.appArgs.configPath, "addons")
		for dir in os.listdir(addonPath):
			path = os.path.join(addonPath, dir, "manifest.ini")
			with open(path, "r", encoding = "utf-8") as f:
				content = f.read()
			content = reg.sub(f" = {self._yearCompatibilityChoice.GetStringSelection()}.1", content)
			with open(path, "w", encoding = "utf-8") as f:
				f.write(content)
		wx.CallAfter(promptUserForRestart)

