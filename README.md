# mcef-codec-patch
Patch JCEF binaries for MCEF to enable support for proprietary codecs such as AVC and MPEG-4.

<img src="https://imgur.com/HvImTGc.png" width="300">

## Instructions
Before you use this tool, ensure MCEF (Ruinscraft fork, 1.31) has been installed and has been run at least once. You should test to make sure everything's working before trying to patch it.

After ensuring MCEF works, set `B:skipUpdates=false` in the MCEF config (By default located in `.minecraft/config/mcef.cfg`). If you don't do this, MCEF will just override the patched files when you launch Minecraft.

1. Download the latest release from the Releases page on GitHub
2. Extract the downloaded .zip file
3. Navigate to the extracted folder and run the "patch" program
4. Choose your Minecraft install location if it isn't the default by clicking "Choose"
5. Click "Patch" and wait until it finishes
6. Close the program and test it out in Minecraft!
