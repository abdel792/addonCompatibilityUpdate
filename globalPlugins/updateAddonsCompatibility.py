import globalPluginHandler
import wx
import gui
import core
import os
from scriptHandler import script

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

class GlobalPlugin (globalPluginHandler.GlobalPlugin):

	@script(description = "Permet de mettre à jour la compatibilité des extensions jusqu'à NVDA de 2030",
	gesture = "kb:control+shift+u"
	)
	def script_updateAddonCompatibility (self, gesture):
		import re
		import globalVars
		ptrn = r"(?<=lastTestedNVDAVersion).+$"
		rgx = re.compile(ptrn, re.M)
		addonPath = os.path.join(globalVars.appArgs.configPath, "addons")
		for dir in os.listdir(addonPath):
			path = os.path.join(addonPath, dir, "manifest.ini")
			with open(path, "r", encoding = "utf-8") as f:
				content = f.read()
			content = rgx.sub(" = 2030.1", content)
			with open(path, "w", encoding = "utf-8") as f:
				f.write(content)
		wx.CallAfter(promptUserForRestart)
