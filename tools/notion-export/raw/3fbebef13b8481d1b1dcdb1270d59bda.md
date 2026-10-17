<!-- meta: {"id": "3fbebef13b8481d1b1dcdb1270d59bda", "title": "How to Clean Install macOS Sequoia", "parent": "3fbebef13b8481a2a2cadb45f1bed830", "truncated": false, "unknown_block_ids": [], "last_edited": "2026-10-16T08:48:44.442Z"} -->
<page>
<content>
# Sources
- [ ] **How to download and install macOS (Apple)**
	[support.apple.com/en-lk/102662](https://support.apple.com/en-lk/102662)
- [ ] **Create a bootable installer for macOS (Apple)**
	[support.apple.com/en-lk/101578](https://support.apple.com/en-lk/101578)
- [ ] **Find out which macOS your Mac is using – latest versions (Apple)**
	[support.apple.com/en-lk/109033#latest](https://support.apple.com/en-lk/109033#latest)
- [ ] **How to Clean Install macOS Sequoia (CleverFiles)**
	[cleverfiles.com/howto/clean-install-macos-sequoia.html](https://www.cleverfiles.com/howto/clean-install-macos-sequoia.html)
- [ ] **Downgrade Tahoe to Sequoia – Step-by-Step (Mr. Macintosh, YouTube)**
	[youtube.com/watch?v=uQ4RZHehp0k](https://www.youtube.com/watch?v=uQ4RZHehp0k)
- [ ] **How to Downgrade macOS to an Older Version (AnsonAlex)**
	[ansonalex.com/tutorials/downgrade-macos](https://ansonalex.com/tutorials/downgrade-macos/)
---
<callout icon="🎯" color="blue_bg">
	**Goal:** clean install **macOS Sequoia 15.8.1** (latest Sequoia) on a **MacBook Air M1** currently running **macOS 27 Golden Gate 27.0.1**, using a bootable USB flash drive.
	**Time:** about 2–3 hours plus backup time. **Needs:** 32 GB+ USB drive, charger, stable Wi-Fi.
</callout>
<callout icon="⚠️" color="red_bg">
	**This is a downgrade, so the internal drive must be erased.** Apple doesn't support going back to an older macOS without erasing.
	**Time Machine won't help here:** a backup made on macOS 27 can't be restored into macOS 15. Back up files manually or to the cloud and copy them back by hand afterwards.
	**Don't use Recovery's "Reinstall macOS"** for this. On this Mac it would reinstall macOS 27, not Sequoia.
</callout>
<table_of_contents/>
# How the sources fit together
<table fit-page-width="true" header-row="true">
<tr>
<td>Step</td>
<td>Main source</td>
</tr>
<tr>
<td>Latest Sequoia version (15.8.1)</td>
<td>Apple: Find out which macOS your Mac is using</td>
</tr>
<tr>
<td>Downloading the full Sequoia installer</td>
<td>Apple: How to download and install macOS</td>
</tr>
<tr>
<td>Making the USB installer and booting from it</td>
<td>Apple: Create a bootable installer for macOS</td>
</tr>
<tr>
<td>Downgrade order, erasing on Apple silicon, Activate Mac screen</td>
<td>Mr. Macintosh video (timestamps linked below)</td>
</tr>
<tr>
<td>Backups, licences, Time Machine caveat</td>
<td>CleverFiles guide, AnsonAlex downgrade guide</td>
</tr>
</table>
# Phase 1: Prepare the Mac
- [ ] Confirm compatibility: MacBook Air M1 (2020) supports Sequoia ([Apple compatibility list](https://support.apple.com/en-lk/120282))
- [ ] Charger plugged in, stable Wi-Fi available. On Apple silicon the installer must reach Apple's servers during install
- [ ] USB drive (32 GB+) with nothing important on it. The M1 Air only has USB-C ports, so use a USB-C drive or a simple USB-C adapter plugged **directly** into the Mac (no hubs)
## Back up your data (manual / cloud)
Video: [Backup your data first](https://www.youtube.com/watch?v=uQ4RZHehp0k&t=119s)
- [ ] Turn on iCloud Drive **Desktop & Documents** sync, or upload folders to Google Drive / OneDrive
- [ ] Photos: make sure iCloud Photos has finished syncing, or export originals to the cloud
- [ ] Projects not in Git: push them, or zip and upload
- [ ] SSH keys: copy the whole `.ssh` folder from your home folder (store it encrypted, e.g. inside a password-protected zip)
- [ ] Dotfiles: `.zshrc`, `.gitconfig`, `.zprofile`, editor settings (VS Code Settings Sync can handle its own)
- [ ] Homebrew list: run `brew bundle dump --file ~/Brewfile` and upload the `Brewfile`
- [ ] App list: run `ls /Applications > ~/apps.txt` and upload it
- [ ] Browser bookmarks and passwords synced (iCloud Keychain, Chrome sync, or a password manager)
- [ ] **Verify** the files open from another device or the web before going further
## Sign out and deactivate
- [ ] Deactivate paid app licences that limit activations (look for "Deactivate" or "Sign Out" in each app's settings)
- [ ] Sign out of iCloud and turn off Find My: System Settings › your name › Sign Out ([video](https://www.youtube.com/watch?v=uQ4RZHehp0k&t=99s)). Do this **after** iCloud uploads have finished
- [ ] Sign out of Messages and FaceTime
# Phase 2: Download the full Sequoia installer
Do this on the M1 itself while it's still running macOS 27. Video: [Download installer](https://www.youtube.com/watch?v=uQ4RZHehp0k&t=353s)
1. Open **Terminal** and list what Apple offers for this Mac:
	```bash
softwareupdate --list-full-installers
	```
2. Download the latest Sequoia (15.8.1 at the time of writing; use the newest 15.x in the list):
	```bash
softwareupdate --fetch-full-installer --full-installer-version 15.8.1
	```
3. Check **Applications** for **Install macOS Sequoia**. It's a large app (well over 10 GB). If it opens by itself, quit it. Don't click Continue.
**Alternative:** open the macOS Sequoia App Store link on [Apple's download page](https://support.apple.com/en-lk/102662) and click **Get**, then quit the installer when it opens.
# Phase 3: Create the bootable USB installer
Video: [Format the USB drive](https://www.youtube.com/watch?v=uQ4RZHehp0k&t=301s) · [Create the installer](https://www.youtube.com/watch?v=uQ4RZHehp0k&t=377s)
1. Plug in the USB drive. Open **Disk Utility**, choose **View › Show All Devices**, select the USB device and click **Erase**:
	- Name: `MyVolume`
	- Format: **Mac OS Extended (Journaled)**
	- Scheme: **GUID Partition Map**
2. In Terminal, run:
	```bash
sudo /Applications/Install\ macOS\ Sequoia.app/Contents/Resources/createinstallmedia --volume /Volumes/MyVolume
	```
3. Enter your admin password (nothing shows as you type), then type `Y` and press Return.
4. If asked whether Terminal may access a removable volume, click **OK**.
5. Wait until Terminal says the install media is available. The drive is now named **Install macOS Sequoia**.
6. Eject the drive. Your Mac is still on macOS 27 at this point; nothing has been erased yet.
# Phase 4: Boot from the USB and erase the Mac
<callout icon="🛑" color="yellow_bg">
	**Last chance:** check your backup one more time. Everything below erases the internal drive.
</callout>
Video: [Boot to startup options on Apple silicon](https://www.youtube.com/watch?v=uQ4RZHehp0k&t=512s) · [Select the USB installer](https://www.youtube.com/watch?v=uQ4RZHehp0k&t=589s)
1. **Shut down** the Mac.
2. Plug the USB installer directly into the Mac.
3. Press and **hold the power button** until "Loading startup options" appears.
4. Select **Install macOS Sequoia** › **Continue**. If asked, choose your admin user and enter its password.
## Erase Macintosh HD
Video: [Erase Macintosh HD on Apple silicon](https://www.youtube.com/watch?v=uQ4RZHehp0k&t=623s)
1. In the installer window, open **Disk Utility**.
2. Select **Macintosh HD** in the sidebar and click **Erase**.
3. Name: `Macintosh HD` · Format: **APFS**.
4. Click **Erase Volume Group** (not just Erase). Enter your Apple ID if asked to turn off Activation Lock.
5. Erase the **Macintosh HD volume group only**. Don't erase or delete other internal containers; on Apple silicon those hold recovery and system files.
## Activate the Mac
Video: [Activate Mac screen](https://www.youtube.com/watch?v=uQ4RZHehp0k&t=677s)
- [ ] After erasing, the Mac restarts and shows **Activate Mac**. Connect to Wi-Fi and sign in with your Apple ID if asked. This is normal on Apple silicon
- [ ] If it starts up in the internal recovery instead of the USB, shut down and choose the USB again from startup options ([video](https://www.youtube.com/watch?v=uQ4RZHehp0k&t=740s))
# Phase 5: Install macOS Sequoia
Video: [Start the Sequoia installer](https://www.youtube.com/watch?v=uQ4RZHehp0k&t=716s) · [Installer screens](https://www.youtube.com/watch?v=uQ4RZHehp0k&t=780s)
1. In the installer window, choose **Install macOS Sequoia** › **Continue**.
2. Agree to the licence and choose **Macintosh HD** as the destination.
3. Wait. It takes 30–60 minutes and restarts several times. Keep the charger in and the lid open.
4. If the progress bar seems stuck, wait at least 30 minutes before doing anything.
# Phase 6: First setup
Video: [Setup Assistant and creating an account](https://www.youtube.com/watch?v=uQ4RZHehp0k&t=885s)
- [ ] Country, language, Wi-Fi
- [ ] **Migration Assistant: choose "Not now"**. This keeps the install clean, and a macOS 27 backup can't be migrated anyway
- [ ] Sign in with your Apple ID and create your user account
- [ ] Turn on **FileVault**
- [ ] Apple menu › **About This Mac**: confirm it says **macOS Sequoia 15.8.1**
- [ ] System Settings › General › Software Update: install any **Sequoia 15.x** update. Don't click the macOS 27 upgrade
# Phase 7: Restore your data manually
Video: [Manually restore files](https://www.youtube.com/watch?v=uQ4RZHehp0k&t=939s)
- [ ] Sign back in to iCloud; let Desktop & Documents and Photos download
- [ ] Download project folders and other files from the cloud
- [ ] Copy only what you need. Don't copy `Library` folders from macOS 27; let apps recreate their own settings
- [ ] Reactivate app licences
# Phase 8: Developer setup
1. Command line tools (includes Git):
	```bash
xcode-select --install
	```
2. Homebrew:
	```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
	```
	Then follow the "Next steps" lines it prints to add Homebrew to your PATH.
3. Reinstall your packages and apps from the saved list:
	```bash
brew bundle --file ~/Brewfile
	```
4. Restore SSH keys (put the `.ssh` folder back in your home folder first):
	```bash
chmod 700 ~/.ssh
chmod 600 ~/.ssh/id_*
chmod 644 ~/.ssh/*.pub
ssh-add --apple-use-keychain ~/.ssh/id_ed25519
	```
5. Restore dotfiles (`.zshrc`, `.gitconfig`) and check with `git config --global --list`.
6. Reinstall remaining apps from `apps.txt` and re-sign in to VS Code / editor sync.
# Phase 9: Stay on Sequoia
- [ ] System Settings › General › Software Update › **Automatic updates (ⓘ)**
	- Turn **off** "Download new updates when available"
	- Turn **off** "Install macOS updates"
	- Keep **on** "Install Security Responses and system files"
- [ ] When updating, use **Update Now** (15.x updates). **Upgrade Now** means macOS 27
- [ ] Ignore macOS 27 prompts in Software Update and the App Store. A personal Mac can't fully hide them without device management, so just don't click them
- [ ] Apple usually gives security updates to the two previous macOS versions. Keep installing 15.x updates, and plan to move up when Sequoia's support ends
# Troubleshooting
<details>
<summary>"softwareupdate: Update not found" when downloading</summary>
	The version number isn't offered for this Mac. Run `softwareupdate --list-full-installers` and use a 15.x version exactly as listed, or use the App Store link on Apple's download page.
</details>
<details>
<summary>"Does not appear to be a valid installer application"</summary>
	The download is incomplete or a small stub. Delete Install macOS Sequoia, download it again with `softwareupdate`, then rerun createinstallmedia.
</details>
<details>
<summary>"Command not found" or the volume can't be found</summary>
	Check the installer is in **Applications** and named exactly **Install macOS Sequoia**, and the USB drive is named exactly `MyVolume`. Run `diskutil list` to see what's mounted.
</details>
<details>
<summary>The USB installer doesn't appear in startup options</summary>
	Plug the drive directly into the Mac (no hub), try the other USB-C port, and hold the power button longer. If it still doesn't show, recreate the installer, or try another drive.
</details>
<details>
<summary>Installer error such as "An error occurred preparing the software update" or a personalisation failure</summary>
	The Mac must be online during install on Apple silicon. Check Wi-Fi, restart from the USB and try again. Make sure you used **Erase Volume Group** on Macintosh HD. If it keeps failing, use the DFU rescue below.
</details>
<details>
<summary>Circle with a line through it at startup</summary>
	The installer doesn't match this Mac or is damaged. Recreate the USB from a fresh Sequoia download.
</details>
<details>
<summary>Mac keeps starting up in the internal recovery</summary>
	Shut down, hold the power button, and select **Install macOS Sequoia** from startup options again. Don't use the internal recovery's "Reinstall macOS"; that would install macOS 27.
</details>
<details>
<summary>DFU rescue: the Mac won't start or install at all</summary>
	As a last resort an Apple silicon Mac can be revived or restored in DFU mode using **Apple Configurator** on **a second Mac** and a USB-C cable ([Apple guide](https://support.apple.com/en-us/108900)). A restore erases everything and can install a macOS IPSW file directly.
	You don't have a second Mac, so if you get here: borrow a Mac from a friend, or take it to an Apple Authorised Service Provider, who can do the restore.
</details>
</content>
</page>
