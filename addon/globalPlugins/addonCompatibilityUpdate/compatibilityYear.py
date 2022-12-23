# -*- coding: utf-8 -*-
# addonCompatibilityUpdate Add-on for NVDA
# compatibilityYear.py.
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

class CompatibilityYearSettingsDialog(SettingsDialog):

	# Translators: This is the label for the compatibility years settings panel.
	title = _("List of years to choose for add-on compatibility")

	def makeSettings(self, settingsSizer):
		self._compatibilityYearChoices = tuple([str(x) for x in range (versionInfo.version_year, versionInfo.version_year + 11)])

		# Translators: This is the label for a combo box in the Compatibility year settings dialog.
		self._compatibilityYearTitle = _("C&ompatibility years for add-ons:")

		self.showCompatibilityYearDialog(settingsSizer=settingsSizer)

	def postInit(self):
		self._compatibilityYearChoice.SetFocus()

	def showCompatibilityYearDialog(self, settingsSizer):
		compatibilityYearSettingsGuiHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		self._compatibilityYearChoice = compatibilityYearSettingsGuiHelper.addLabeledControl(
			self._compatibilityYearTitle, wx.Choice, choices=self._compatibilityYearChoices
		)

		curChoice = config.conf["addonCompatibilityUpdate"]["compatibilityYearChoice"]
		for index, name in enumerate(self._compatibilityYearChoices):
			if name == curChoice:
				self._compatibilityYearChoice.SetSelection(index)
				break

	def onOk(self, evt):
		super(CompatibilityYearSettingsDialog, self).onOk(evt)
		config.conf["addonCompatibilityUpdate"]["compatibilityYearChoice"] = self._compatibilityYearChoice.GetStringSelection()
		ptrn = r"(?<=lastTestedNVDAVersion)[0-9\.]+"
		rgx = re.compile(ptrn, re.M)
		addonPath = os.path.join(globalVars.appArgs.configPath, "addons")
		for dir in os.listdir(addonPath):
			if not dir == "updateAddonsCompatibility":
				path = os.path.join(addonPath, dir, "manifest.ini")
				with open(path, "r", encoding = "utf-8") as f:
					content = f.read()
				content = rgx.sub(f" = {self._compatibilityYearChoice.GetStringSelection()}.1", content)
				with open(path, "w", encoding = "utf-8") as f:
					f.write(content)
		wx.CallAfter(promptUserForRestart)

