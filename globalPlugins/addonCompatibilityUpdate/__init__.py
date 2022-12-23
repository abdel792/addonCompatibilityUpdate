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
from .compatibleYear import CompatibleYearSettingsDialog

confspec = {
	"compatibleYearChoice": f"string(default={versionInfo.version_year})",
}
config.conf.spec["addonCompatibilityUpdate"] = confspec

class GlobalPlugin (globalPluginHandler.GlobalPlugin):

	scriptCategory = addonHandler.getCodeAddon().manifest["summary"]

	def __init__(self):
		super(globalPluginHandler.GlobalPlugin, self).__init__()
		if globalVars.appArgs.secure or config.isAppX:
			return
		self.toolsMenu = gui.mainFrame.sysTrayIcon.toolsMenu
		self.compatibleYearSettings = self.toolsMenu.Append(
			# Translators: The name of the compatible years item in NVDA Tools menu.
			wx.ID_ANY, _("Com&patible years..."),
			# Translators: The tooltyp text for the compatible years item in NVDA Tools menu.
			_("Allows you to choose your compatible year")
		)
		gui.mainFrame.sysTrayIcon.Bind(wx.EVT_MENU, self.onCompatibleYearSettingsDialog, self.compatibleYearSettings)

	def terminate(self):
		super(GlobalPlugin, self).terminate()
		try:
			self.toolsMenu.Remove(self.compatibleYearSettings)
		except (RuntimeError, AttributeError):
			pass


	def onCompatibleYearSettingsDialog(self, evt):
		try:
			gui.mainFrame.prePopup()
			d = CompatibleYearSettingsDialog(gui.mainFrame)
			d.Show()
			gui.mainFrame.postPopup()
		except gui.settingsDialogs.SettingsDialog.MultiInstanceErrorWithDialog:
			wx.CallAfter(
				gui.messageBox,
				# Translators: error message when attempting to open more than one compatible year settings dialogs.
				_("Compatible year dialog is already open."),
				skipTranslation.translate("Error"), wx.OK | wx.ICON_ERROR
			)

	@script(
		# Translators: Message presented in input help mode.
		description=_("Display the Compatible year settings dialog box.")
	)
	def script_activateCompatibleYearSettingsDialog(self, gesture):
		wx.CallAfter(self.onCompatibleYearSettingsDialog, None)


