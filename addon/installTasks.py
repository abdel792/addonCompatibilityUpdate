# -*- coding: UTF-8 -*-

# installTasks.py.

# Copyright 2022-2023 Abdelkrim Bensaïd, released under gPL.
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import addonHandler
import gui
import wx
addonHandler.initTranslation()

def onInstall():
	addon = [x for x in addonHandler.getAvailableAddons() if x.manifest["name"] == "updateAddonsCompatibility"]
	if len(addon) > 0:
		addon = addon[0]
		if gui.messageBox(
		# Translators: A message informing the user that he has installed an incompatible version.
		_("You have installed the updateAddonsCompatibility add-on which is incompatible with this one. Do you want to uninstall this old version?"),
		# Translators: The title of the dialogbox.
		_("Uninstall incompatible version"),
		wx.YES|wx.NO|wx.ICON_WARNING)==wx.YES:
			addon.requestRemove()
