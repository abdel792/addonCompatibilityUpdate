import versionInfo
import os
import re
import globalVars
import core
import gui
import config
from gui import SettingsPanel, SettingsDialog
import wx

def promptUserForRestart():
	restartMessage = _(
		# Translators: A message asking the user if they wish to restart NVDA
		# as addons have been added, enabled/disabled or removed.
		"Changes were made to add-ons. "
		"You must restart NVDA for these changes to take effect. "
		"Would you like to restart now?"
	)
	# Translators: Title for message asking if the user wishes to restart NVDA as addons have been added or removed.
	restartTitle = _("Restart NVDA")
	result = gui.messageBox(
		message=restartMessage,
		caption=restartTitle,
		style=wx.YES | wx.NO | wx.ICON_WARNING
	)
	if wx.YES == result:
		core.restart()

class CompatibleYearSettingsDialog(SettingsDialog):

	# Translators: This is the label for the compatible years settings panel.
	title = _("Compatible years")

	def makeSettings(self, settingsSizer):
		self._compatibleYearChoices = tuple([str(x) for x in range (versionInfo.version_year, versionInfo.version_year + 11)])

		# Translators: This is the label for a combo box in the Compatible year settings dialog.
		self._compatibleYearTitle = _("C&ompatible years:")

		self.showCompatibleYearDialog(settingsSizer=settingsSizer)

	def postInit(self):
		self._compatibleYearChoice.SetFocus()

	def showCompatibleYearDialog(self, settingsSizer):
		compatibleYearSettingsGuiHelper = gui.guiHelper.BoxSizerHelper(self, sizer=settingsSizer)
		self._compatibleYearChoice = compatibleYearSettingsGuiHelper.addLabeledControl(
			self._compatibleYearTitle, wx.Choice, choices=self._compatibleYearChoices
		)

		curChoice = config.conf["addonCompatibilityUpdate"]["compatibleYearChoice"]
		for index, name in enumerate(self._compatibleYearChoices):
			if name == curChoice:
				self._compatibleYearChoice.SetSelection(index)
				break

	def onOk(self, evt):
		super(CompatibleYearSettingsDialog, self).onOk(evt)
		config.conf["addonCompatibilityUpdate"]["compatibleYearChoice"] = self._compatibleYearChoice.GetStringSelection()
		ptrn = r"(?<=lastTestedNVDAVersion).+$"
		rgx = re.compile(ptrn, re.M)
		addonPath = os.path.join(globalVars.appArgs.configPath, "addons")
		for dir in os.listdir(addonPath):
			if not dir == "updateAddonsCompatibility":
				path = os.path.join(addonPath, dir, "manifest.ini")
				with open(path, "r", encoding = "utf-8") as f:
					content = f.read()
				content = rgx.sub(f" = {self._compatibleYearChoice.GetStringSelection()}.1", content)
				with open(path, "w", encoding = "utf-8") as f:
					f.write(content)
		wx.CallAfter(promptUserForRestart)

