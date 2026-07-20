#!/bin/bash

# ===== Colors =====
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# ===== Dependency Check =====
for tool in curl nmap openssl whois; do
    if ! command -v $tool &> /dev/null; then
        echo -e "${RED}[ERROR] $tool not installed. Install it first.${NC}"
        exit
    fi
done

echo -e "${GREEN}[OK] All tools ready${NC}"

# ===== Input =====
echo "Enter website (example: example.com):"
read site

# ===== Report File =====
report="scan_report_$site.txt"
echo "Scan Report for $site" > $report
echo "Scan Time: $(date)" >> $report
echo "----------------------------------" >> $report

echo -e "\n${YELLOW}Scanning $site ...${NC}"
echo "----------------------------------"

# ===== Reachability =====
echo "[+] Checking reachability..."
curl -Is https://$site > /dev/null 2>&1 || curl -Is http://$site > /dev/null 2>&1

if [ $? -eq 0 ]; then
    echo -e "${GREEN}[OK] Site reachable${NC}"
    echo "[OK] Site reachable" >> $report
else
    echo -e "${RED}[ERROR] Site not reachable${NC}"
    echo "[ERROR] Site not reachable" >> $report
    exit
fi

# ===== HTTP Status Code =====
status=$(curl -o /dev/null -s -w "%{http_code}" http://$site)
echo -e "\n[+] HTTP Status Code: $status"
echo "HTTP Status Code: $status" >> $report

# ===== Port Scan =====
echo -e "\n[+] Scanning ports..."
nmap $site | tee -a $report

# ===== Headers =====
echo -e "\n[+] Fetching headers..."
headers=$(curl -s -I https://$site || curl -s -I http://$site)
echo "$headers"
echo "$headers" >> $report

# ===== Header Checks =====
echo -e "\n[+] Security header analysis..."
echo "Security Header Analysis:" >> $report

check_header() {
    if echo "$headers" | grep -qi "$1"; then
        echo -e "${GREEN}[OK] $2 present${NC}"
        echo "[OK] $2 present" >> $report
    else
        echo -e "${RED}[VULN] Missing $2${NC}"
        echo "[VULN] Missing $2" >> $report
    fi
}

check_header "X-Frame-Options" "X-Frame-Options"
check_header "Content-Security-Policy" "CSP"
check_header "Strict-Transport-Security" "HSTS"
check_header "X-Content-Type-Options" "X-Content-Type-Options"
check_header "Referrer-Policy" "Referrer-Policy"

# ===== HTTPS Check =====
echo -e "\n[+] Checking HTTPS..."
if curl -Is https://$site > /dev/null 2>&1; then
    echo -e "${GREEN}[OK] HTTPS supported${NC}"
    echo "[OK] HTTPS supported" >> $report
else
    echo -e "${RED}[VULN] No HTTPS support${NC}"
    echo "[VULN] No HTTPS support" >> $report
fi

# ===== SSL Certificate =====
echo -e "\n[+] Checking SSL certificate..."
ssl_info=$(echo | openssl s_client -connect $site:443 2>/dev/null | openssl x509 -noout -dates)
echo "$ssl_info"
echo "$ssl_info" >> $report

# ===== Server Info =====
echo -e "\n[+] Checking server info leakage..."
echo "$headers" | grep -i "Server" | tee -a $report
echo "[INFO] Server info exposed" >> $report

# ===== WHOIS =====
echo -e "\n[+] WHOIS info (short)..."
whois $site | head -n 10 | tee -a $report

# ===== robots.txt =====
echo -e "\n[+] Checking robots.txt..."
robots=$(curl -s http://$site/robots.txt)
if echo "$robots" | grep -q "Disallow"; then
    echo -e "${YELLOW}[INFO] robots.txt found${NC}"
    echo "[INFO] robots.txt found" >> $report
else
    echo -e "${GREEN}[OK] No robots.txt or empty${NC}"
    echo "[OK] No robots.txt" >> $report
fi

# ===== Directory Scan =====
echo -e "\n[+] Checking common directories..."
for dir in admin login dashboard config backup; do
    status=$(curl -o /dev/null -s -w "%{http_code}" http://$site/$dir)
    if [ "$status" = "200" ]; then
        echo -e "${RED}[VULN] Found: /$dir${NC}"
        echo "[VULN] Found: /$dir" >> $report
    fi
done

# ===== XSS Test =====
echo -e "\n[+] Testing basic XSS..."
payload="<script>alert(1)</script>"
response=$(curl -s "http://$site/?q=$payload")

if echo "$response" | grep -q "$payload"; then
    echo -e "${RED}[VULN] Possible XSS detected${NC}"
    echo "[VULN] Possible XSS detected" >> $report
else
    echo -e "${GREEN}[OK] No simple XSS${NC}"
    echo "[OK] No simple XSS" >> $report
fi

# ===== Done =====
echo "----------------------------------"
echo -e "${GREEN}Scan Completed! Report saved as $report${NC}"
