# iPhone 6S DFU Mode & Checkra1n Jailbreak Guide

## Device Information
- **Device**: iPhone 6S
- **Chipset**: A9 (vulnerable to checkm8)
- **Compatible iOS**: 12.0 - 14.8.1
- **Jailbreak Type**: Semi-tethered (persistent after reboot)

---

## Step 1: Prepare Your Device

### On iPhone 6S:
1. **Unlock** your iPhone
2. **Connect USB cable** to your PC
3. When prompted: **Tap "Trust"** to allow computer access
4. **Unlock again** if required

### On Your PC:
- Automation script is ready at: `/home/user/obsidian-vault/checkra1n_automate.sh`
- All dependencies installed ✓

---

## Step 2: Enter DFU Mode (Device Firmware Update)

DFU mode is required for Checkra1n to exploit the checkm8 vulnerability.

### For iPhone 6S - DFU Mode Entry:
1. **Phone must be connected** via USB
2. **Press and hold Volume Up button**
3. **Press and hold Volume Down button** (while holding Volume Up)
4. **Press and hold Power/Side button** (while holding both volume buttons)
5. **Release only the Power button** when Apple logo appears
6. **Keep Volume buttons held** until "Connect to iTunes" screen appears
7. **Release all buttons**

**Expected Result**: Screen shows "Connect to iTunes" or blank black screen

### Verify DFU Mode:
Your PC will detect the device in DFU mode and display "Apple USB Device" in device list.

---

## Step 3: Run the Automation Script

Once device is in DFU mode:

```bash
/home/user/obsidian-vault/checkra1n_automate.sh
```

The script will:
1. ✓ Detect iPhone 6S in DFU mode
2. ✓ Download Checkra1n binary
3. ✓ Verify device compatibility
4. ✓ Execute jailbreak exploit
5. ✓ Monitor progress
6. ✓ Verify installation

---

## What Happens During Jailbreak

**Timeline**: ~10-15 minutes

1. **Device will reboot multiple times** - This is normal
2. **Screen will go black** - Expected behavior
3. **"Connect to iTunes" may reappear** - Device auto-recovers
4. **Final reboot** - Device returns to normal state
5. **Cydia appears** - Jailbreak successful!

### Do NOT:
- ❌ Disconnect USB cable
- ❌ Force restart device
- ❌ Lock/unlock during process
- ❌ Use device for other tasks

---

## Post-Jailbreak

### If Successful:
- **Cydia** app appears on home screen
- Can install tweaks and modifications
- Semi-tethered = reboot-persistent

### If Failed:
- Return to DFU mode (repeat Step 2)
- Run script again
- Check iOS version is 12.0-14.8.1
- Try different USB cable/port

---

## Troubleshooting

### Device Not Detected:
- Try different USB port (preferably USB 3.0)
- Try different USB cable
- Unplug all USB devices, try again
- Restart PC

### DFU Mode Entry Failed:
- Practice the button combination first
- Be precise with timing
- Hold buttons longer (5-10 seconds minimum)
- Refer to Step 2 again

### Jailbreak Hangs:
- Wait at least 5 minutes (process is slow)
- Check device screen for prompts
- If truly stuck: Force restart and retry DFU mode

---

## Important Notes

⚠️ **Backup First**: This jailbreak is safe but always backup first
⚠️ **iOS Version**: Only works on iOS 12.0-14.8.1
⚠️ **Irreversible Until Reboot**: Semi-tethered means it persists until device needs DFU again
⚠️ **No Warranty**: Apple may refuse service on jailbroken devices

---

## Quick Command Reference

**Check device connection:**
```bash
lsusb | grep -i apple
```

**View automation logs:**
```bash
cat /tmp/checkra1n_work/checkra1n.log
```

**View work directory:**
```bash
ls -la /tmp/checkra1n_work/
```

**Run automation again:**
```bash
/home/user/obsidian-vault/checkra1n_automate.sh
```

---

## Still Need Help?

1. Check `/tmp/checkra1n_work/checkra1n.log` for errors
2. Ensure device is in DFU mode (black screen or "Connect to iTunes")
3. Try different USB cable/port
4. Restart PC and try again
5. Refer to https://checkra.in for official documentation
