"""
mcef-codec-patch
"""
MCEF_VERSION = "1.31"
PATCHES_DIR = "patches"

from hash import sha1_of_file
import os
import sys

if sys.platform == "linux":
    cef_platform = "linux64"
elif sys.platform == "darwin":
    cef_platform = "mac64"
elif sys.platform == "win32":
    cef_platform = "win64"
else:
    print("Unsupported platform")
    sys.exit()

# Ex: "patches/1.30/linux64"
patches_platform_path = os.path.join(PATCHES_DIR, MCEF_VERSION, cef_platform)

if not os.path.exists(patches_platform_path):
    print("Could not find patches directory")
    sys.exit()

patched_manifest_file = open(os.path.join(patches_platform_path, "patched_manifest.txt"), "r")
patched_manifest = patched_manifest_file.readlines()

diff_manifest_file = open(os.path.join(patches_platform_path, "diff_manifest.txt"), "r")
diff_manifest = diff_manifest_file.readlines()

def apply_patch_to_file(jcef_path, file, log):
    # Search the diff manifest for the file that needs patching
    for line_entry in diff_manifest:
        patch_file = line_entry.split()[0]
        
        if file == patch_file[:-7]:
            file_path = os.path.join(jcef_path, file)
            import bsdiff4
            wx.CallAfter(log.write, "Patching " + file_path + "\n")
            patch_path = os.path.join(patches_platform_path, "Release", patch_file)
            bsdiff4.file_patch_inplace(file_path, patch_path)
            wx.CallAfter(log.write, "Done\n")

def patch(minecraft_location, log, button):
    wx.CallAfter(button.Disable)

    jcef_path = os.path.join(minecraft_location, "jcef")
    total_patched = 0

    if not os.path.exists(jcef_path):
        wx.CallAfter(log.write, "\n\n\nNo path 'jcef' found in Minecraft installation\n")
        wx.CallAfter(log.write, "Ensure MCEF (1.30+) is installed and has been run at least once\n")
        wx.CallAfter(button.Enable)
        return

    for line_entry in patched_manifest:
        file = line_entry.split()[0]
        sha1_hash = line_entry.split()[1]
        file_path = os.path.join(jcef_path, file)

        if os.path.exists(file_path):
            import hash
            if hash.sha1_of_file(file_path) == sha1_hash:
                wx.CallAfter(log.write, file_path + " does not need patching\n")
            else:
                apply_patch_to_file(jcef_path, file, log)
                total_patched = total_patched + 1
        else:
            wx.CallAfter(log.write, file_path + " does not exist!\n")

    wx.CallAfter(log.write, "\n\n\nFinished! Patched " + str(total_patched) + " files\n")
    wx.CallAfter(log.write, "Before launching Minecraft, ensure to edit the MCEF config to skip updates!\n")
    wx.CallAfter(log.write, "The default MCEF config is located in '.minecraft/config/mcef.cfg'\n")
    wx.CallAfter(button.Enable)

import mc_finder
import wx

class MainFrame(wx.Frame):

    def __init__(self, parent, title):
        super(MainFrame, self).__init__(parent, title=title, size=(600, 400))

        self.InitUI()
        self.Centre()

    def InitUI(self):
        panel = wx.Panel(self)
        sizer = wx.GridBagSizer(4, 4)

        text1 = wx.StaticText(panel, label="Minecraft Location")
        sizer.Add(text1, pos=(0, 0), flag=wx.TOP|wx.LEFT|wx.BOTTOM)
        
        minecraft_location = mc_finder.find_minecraft()
        self.mcLocText = wx.TextCtrl(panel, value=minecraft_location)
        sizer.Add(self.mcLocText, pos=(1, 0), span=(1, 4), flag=wx.EXPAND|wx.LEFT|wx.RIGHT)
        mcLocButton = wx.Button(panel, label="Choose")
        mcLocButton.Bind(wx.EVT_BUTTON, self.onChooseButtonPress) 
        sizer.Add(mcLocButton, pos=(1, 4))

        self.log = wx.TextCtrl(panel, style=wx.TE_MULTILINE|wx.TE_READONLY|wx.HSCROLL)
        sizer.Add(self.log, pos=(2, 0), span=(1, 5), flag=wx.EXPAND|wx.LEFT|wx.RIGHT)

        self.patchButton = wx.Button(panel, label="Patch")
        self.patchButton.Bind(wx.EVT_BUTTON, self.onPatchButtonPress) 
        sizer.Add(self.patchButton, pos=(3, 4))

        sizer.AddGrowableCol(1)
        sizer.AddGrowableCol(2)
        sizer.AddGrowableRow(2)

        panel.SetSizer(sizer)

    def onChooseButtonPress(self, event):
        dialog = wx.DirDialog(None, "Choose Minecraft Location:")
        if dialog.ShowModal() == wx.ID_OK:
            self.mcLocText.SetValue(dialog.GetPath())
        dialog.Destroy()

    def onPatchButtonPress(self, event):
        import threading
        minecraft_location = self.mcLocText.GetValue()
        patchThread = threading.Thread(target=patch, args=(minecraft_location, self.log, self.patchButton))
        patchThread.start()

mcpApp = wx.App()
mainFrame = MainFrame(None, title='mcef-codec-patch')
wx.MessageBox("mcef-codec-patch Disclaimer\n\n\nThis software contains binary patches for CEF to include additional codecs (AVC & MPEG-4). The end user is responsible for compiling the final binary product via this helper-software. See the Google Chrome license for more info here: https://www.google.com/chrome/terms/", "Message", wx.OK|wx.ICON_INFORMATION)
mainFrame.Show()
mcpApp.MainLoop()
