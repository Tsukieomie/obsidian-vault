#!/bin/bash

################################################################################
# Checkra1n iPhone 6S Jailbreak Automation Script
# Supports: iOS 12.0 - 14.8.1 on A9 processor
################################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
CHECKRA1N_VERSION="0.12.4"
WORK_DIR="/tmp/checkra1n_work"
LOG_FILE="$WORK_DIR/checkra1n.log"

################################################################################
# Helper Functions
################################################################################

print_header() {
    echo -e "${BLUE}========================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}========================================${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ ERROR: $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ WARNING: $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $1" >> "$LOG_FILE"
}

################################################################################
# System Checks
################################################################################

check_system_requirements() {
    print_header "Checking System Requirements"

    log "Starting system requirement checks"

    # Check Python
    if command -v python3 &> /dev/null; then
        PY_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
        print_success "Python 3 found: $PY_VERSION"
        log "Python 3 version: $PY_VERSION"
    else
        print_error "Python 3 not found"
        log "Python 3 not found - installation required"
        return 1
    fi

    # Check libusb
    if pkg-config --exists libusb-1.0; then
        print_success "libusb-1.0 found"
        log "libusb-1.0 is installed"
    else
        print_error "libusb-1.0 not found"
        log "libusb-1.0 not found - installation required"
        return 1
    fi

    # Check gcc
    if command -v gcc &> /dev/null; then
        print_success "GCC compiler found"
        log "GCC compiler is available"
    else
        print_error "GCC compiler not found"
        log "GCC compiler not found"
        return 1
    fi

    print_success "All system requirements met"
    return 0
}

################################################################################
# Device Detection
################################################################################

detect_connected_device() {
    print_header "Detecting Connected Device"

    log "Scanning for connected USB devices"

    # Check if lsusb is available
    if ! command -v lsusb &> /dev/null; then
        print_warning "lsusb not found, attempting to install usbutils..."
        apt-get install -y usbutils 2>&1 | tail -5
        log "Installed usbutils"
    fi

    # List USB devices
    echo -e "\n${BLUE}Connected USB Devices:${NC}"
    lsusb || print_warning "Could not list USB devices"

    # Check for Apple/iPhone devices
    if lsusb 2>/dev/null | grep -qi "apple"; then
        print_success "Apple device detected!"
        log "Apple device found via lsusb"
        return 0
    else
        print_error "No Apple device detected"
        echo -e "\n${YELLOW}Please:${NC}"
        echo "1. Connect iPhone 6S via USB cable"
        echo "2. Unlock iPhone and tap 'Trust' on the prompt"
        echo "3. Run this script again"
        log "No Apple device detected - user intervention required"
        return 1
    fi
}

check_dfu_mode() {
    print_header "Checking DFU Mode Status"

    log "Checking if device is in DFU mode"

    # Look for device in DFU mode (0x1227 for Apple)
    if lsusb 2>/dev/null | grep -qi "1227"; then
        print_success "Device is in DFU mode"
        log "Device detected in DFU mode"
        return 0
    else
        print_warning "Device not in DFU mode"
        echo -e "\n${YELLOW}To enter DFU mode on iPhone 6S:${NC}"
        echo "1. Connect iPhone to computer via USB"
        echo "2. Force restart: Press and hold Volume Up, then Volume Down"
        echo "3. Keep holding both buttons and press/hold Side button (or Power)"
        echo "4. Release when Apple logo appears"
        echo "5. Release buttons when 'Connect to iTunes' screen appears"
        log "Device not in DFU mode - user must manually enter DFU mode"
        return 1
    fi
}

################################################################################
# Checkra1n Download & Verification
################################################################################

download_checkra1n() {
    print_header "Downloading Checkra1n"

    mkdir -p "$WORK_DIR"
    cd "$WORK_DIR"

    log "Creating work directory: $WORK_DIR"

    # Determine architecture
    ARCH=$(uname -m)
    print_info "System architecture: $ARCH"
    log "System architecture: $ARCH"

    if [[ "$ARCH" == "x86_64" ]]; then
        BINARY="checkra1n-x86_64"
    elif [[ "$ARCH" == "aarch64" ]]; then
        BINARY="checkra1n-aarch64"
    else
        print_error "Unsupported architecture: $ARCH (x86_64 or aarch64 required)"
        log "Unsupported architecture: $ARCH"
        return 1
    fi

    print_info "Target binary: $BINARY"
    log "Target binary: $BINARY"

    # Attempt to download from official source
    DOWNLOAD_URL="https://checkra.in/releases/linux/$BINARY"
    print_info "Attempting to download from: $DOWNLOAD_URL"
    log "Download URL: $DOWNLOAD_URL"

    if ! curl -L -o "$BINARY" "$DOWNLOAD_URL" 2>&1 | tee -a "$LOG_FILE"; then
        print_error "Failed to download Checkra1n"
        print_warning "Possible causes: No internet, network restricted, firewall"
        log "Download failed - no internet access or network restricted"
        return 1
    fi

    # Check if file was downloaded
    if [ ! -f "$BINARY" ] || [ ! -s "$BINARY" ]; then
        print_error "Downloaded file is empty or missing"
        log "Downloaded file is empty or missing"
        return 1
    fi

    # Make executable
    chmod +x "$BINARY"
    print_success "Checkra1n downloaded and made executable"
    log "Checkra1n binary ready: $WORK_DIR/$BINARY"

    return 0
}

################################################################################
# Jailbreak Execution
################################################################################

run_jailbreak() {
    print_header "Starting Jailbreak Process"

    cd "$WORK_DIR"
    BINARY=$(ls checkra1n-* 2>/dev/null | head -1)

    if [ -z "$BINARY" ]; then
        print_error "Checkra1n binary not found"
        log "Checkra1n binary not found in $WORK_DIR"
        return 1
    fi

    print_info "Using binary: $BINARY"
    print_info "iOS versions supported: 12.0 - 14.8.1"
    print_info "Device: iPhone 6S (A9 chipset)"

    log "Starting jailbreak with $BINARY"

    echo -e "\n${YELLOW}IMPORTANT:${NC}"
    echo "• Do NOT disconnect USB cable during process"
    echo "• Process may take 10-15 minutes"
    echo "• Device will reboot multiple times"
    echo "• Keep device screen on"
    echo ""

    # Run checkra1n in console mode (no GUI)
    ./"$BINARY" -c 2>&1 | tee -a "$LOG_FILE"

    local exit_code=$?

    if [ $exit_code -eq 0 ]; then
        print_success "Jailbreak completed successfully!"
        log "Jailbreak process completed with exit code: 0"
        return 0
    else
        print_error "Jailbreak process exited with code: $exit_code"
        log "Jailbreak process exited with code: $exit_code"
        return 1
    fi
}

################################################################################
# Post-Jailbreak Verification
################################################################################

verify_jailbreak() {
    print_header "Verifying Jailbreak Status"

    log "Verifying jailbreak installation"

    echo -e "\n${BLUE}Jailbreak verification checklist:${NC}"
    echo "1. Check if Cydia app is present on iPhone home screen"
    echo "2. Open Cydia and verify package manager is working"
    echo "3. If errors occur, try rebooting the device"
    echo ""

    print_info "If jailbreak succeeded:"
    echo "   • Cydia package manager will be installed"
    echo "   • Semi-tethered jailbreak is persistent across reboots"
    echo "   • You can install tweaks and modifications"
    echo ""

    print_info "If jailbreak failed:"
    echo "   • Return device to DFU mode and try again"
    echo "   • Ensure iOS version is 12.0-14.8.1"
    echo "   • Try a different USB cable or port"

    log "Jailbreak verification complete"
}

################################################################################
# Cleanup & Logging
################################################################################

generate_report() {
    print_header "Generating Report"

    echo -e "\n${BLUE}Checkra1n Automation Report${NC}"
    echo "Date: $(date)"
    echo "Log file: $LOG_FILE"
    echo ""
    echo "Summary of operations:"
    echo "• System requirements: Verified"
    echo "• Device detection: Completed"
    echo "• Checkra1n binary: Downloaded and executed"
    echo "• Jailbreak process: Completed"
    echo ""

    if [ -f "$LOG_FILE" ]; then
        echo -e "${BLUE}=== Full Log ===${NC}"
        cat "$LOG_FILE"
    fi
}

################################################################################
# Main Execution Flow
################################################################################

main() {
    print_header "Checkra1n iPhone 6S Jailbreak Automation"

    # Create work directory and log file
    mkdir -p "$WORK_DIR"
    touch "$LOG_FILE"
    log "Script started by user $(whoami)"

    # Step 1: System checks
    if ! check_system_requirements; then
        print_error "System requirements not met"
        log "System requirements check failed"
        return 1
    fi

    # Step 2: Device detection
    if ! detect_connected_device; then
        print_warning "Device detection failed - waiting for device..."
        log "Device detection failed - waiting for user to connect device"
        echo ""
        read -p "Press Enter after connecting iPhone 6S..."

        if ! detect_connected_device; then
            print_error "Still no device detected"
            return 1
        fi
    fi

    # Step 3: DFU mode check
    echo ""
    if ! check_dfu_mode; then
        print_warning "Device not in DFU mode - waiting for user intervention..."
        log "Device not in DFU mode"
        echo ""
        read -p "Press Enter after entering DFU mode on iPhone..."

        if ! check_dfu_mode; then
            print_error "Device still not in DFU mode"
            log "Device still not in DFU mode after user attempt"
            return 1
        fi
    fi

    # Step 4: Download Checkra1n
    echo ""
    if ! download_checkra1n; then
        print_error "Failed to download Checkra1n"
        log "Checkra1n download failed"
        return 1
    fi

    # Step 5: Run jailbreak
    echo ""
    if ! run_jailbreak; then
        print_error "Jailbreak process failed"
        log "Jailbreak execution failed"
        return 1
    fi

    # Step 6: Verify and report
    echo ""
    verify_jailbreak

    # Step 7: Generate report
    echo ""
    generate_report

    print_success "Checkra1n automation script completed!"
    log "Script completed successfully"

    return 0
}

# Run main function
main
exit $?
