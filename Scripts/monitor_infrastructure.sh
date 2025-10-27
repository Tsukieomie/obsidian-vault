#!/bin/bash
#
# Infrastructure Monitoring Script
# Monitors AS53616 network, domains, and infrastructure changes
#
# Usage: ./monitor_infrastructure.sh
# Output: Creates timestamped logs in Logs/ directory
#

set -euo pipefail

# Configuration
LOG_DIR="./Logs"
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)
LOG_FILE="${LOG_DIR}/${TIMESTAMP}_infrastructure_monitor.log"

# Create log directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Domains to monitor
DOMAINS=(
    "ghoststack.net"
    "ca94fan.xyz"
)

# ASN to monitor
ASN="AS53616"

# Initialize log
cat > "$LOG_FILE" << EOF
Infrastructure Monitoring Report
Generated: $(date -u +"%Y-%m-%d %H:%M:%S UTC")
=================================================

EOF

echo "[+] Starting infrastructure monitoring..."
echo "[+] Log file: $LOG_FILE"

# Function to log with timestamp
log() {
    echo "[$(date +%H:%M:%S)] $1" | tee -a "$LOG_FILE"
}

# Function to append to log file
log_append() {
    echo "$1" >> "$LOG_FILE"
}

# Monitor AS53616
log "Checking AS53616 information..."
log_append ""
log_append "=== AS53616 Information ==="
log_append ""

# WHOIS lookup for ASN (using public WHOIS servers)
if command -v whois &> /dev/null; then
    log_append "--- WHOIS Information ---"
    whois -h whois.arin.net "$ASN" >> "$LOG_FILE" 2>&1 || log_append "WHOIS lookup failed"
    log_append ""
else
    log_append "whois command not available - skipping WHOIS lookup"
    log_append ""
fi

# Monitor each domain
for domain in "${DOMAINS[@]}"; do
    log "Checking domain: $domain"
    log_append ""
    log_append "=== Domain: $domain ==="
    log_append ""

    # DNS A records
    log_append "--- DNS A Records ---"
    if command -v dig &> /dev/null; then
        dig +short A "$domain" >> "$LOG_FILE" 2>&1 || log_append "DNS lookup failed"
    elif command -v nslookup &> /dev/null; then
        nslookup "$domain" >> "$LOG_FILE" 2>&1 || log_append "DNS lookup failed"
    else
        log_append "No DNS tools available"
    fi
    log_append ""

    # DNS NS records
    log_append "--- DNS NS Records ---"
    if command -v dig &> /dev/null; then
        dig +short NS "$domain" >> "$LOG_FILE" 2>&1 || log_append "NS lookup failed"
    fi
    log_append ""

    # WHOIS information
    log_append "--- WHOIS Information ---"
    if command -v whois &> /dev/null; then
        whois "$domain" >> "$LOG_FILE" 2>&1 || log_append "WHOIS lookup failed"
    else
        log_append "whois command not available"
    fi
    log_append ""

    # Ping test (basic connectivity)
    log_append "--- Connectivity Test ---"
    if ping -c 3 -W 2 "$domain" >> "$LOG_FILE" 2>&1; then
        log_append "Domain is responding to ping"
    else
        log_append "Domain is not responding to ping (may be normal if ICMP blocked)"
    fi
    log_append ""

    log_append "==========================================="
    log_append ""
done

# Summary
log_append ""
log_append "=== Monitoring Complete ==="
log_append "Report saved to: $LOG_FILE"
log_append "Timestamp: $(date -u +"%Y-%m-%d %H:%M:%S UTC")"

log "Monitoring complete"
log "Results saved to: $LOG_FILE"

# Create latest symlink
ln -sf "$LOG_FILE" "${LOG_DIR}/latest.log"

echo ""
echo "View results: cat $LOG_FILE"
echo "View latest: cat ${LOG_DIR}/latest.log"
