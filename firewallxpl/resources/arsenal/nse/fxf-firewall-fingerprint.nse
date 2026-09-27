-- fxf-firewall-fingerprint.nse
-- Part of FirewallXPL-Forge NSE suite.
--
-- Generic firewall/NGFW/UTM fingerprinting. Probes common management and VPN
-- endpoints for signatures from multiple vendors and reports the best match.
--
-- Usage:
--   nmap -p 443,80,8443,4443,8080 --script fxf-firewall-fingerprint <target>
--   nmap -p 443 --script fxf-firewall-fingerprint \
--       --script-args "fxf.timeout=15,fxf.verbose=1" <target>
--
-- Output example:
--   PORT    STATE SERVICE
--   443/tcp open  https
--   | fxf-firewall-fingerprint:
--   |   Vendor: SonicWall
--   |   Product: SonicOS SSL-VPN
--   |   Confidence: HIGH
--   |   Match path: /auth.html
--   |   Notable CVEs: CVE-2021-20034, CVE-2024-40766
--   |_  fxf modules: exploits/perimeter/sonicwall/
--
-- Author: André Henrique (@mrhenrike) | União Geek
-- License: BSD-3-Clause

local http      = require "http"
local shortport = require "shortport"
local stdnse    = require "stdnse"
local string    = require "string"
local table     = require "table"

description = [[
Generic NGFW/UTM/firewall fingerprinting for FirewallXPL-Forge.

Attempts to identify the firewall vendor by probing known management and VPN paths
across multiple vendors: Palo Alto, Fortinet, Cisco, SonicWall, Sophos, Check Point,
Juniper, Zyxel, pfSense, WatchGuard, and Barracuda.

For detailed vendor-specific checks, use the dedicated scripts:
  fxf-globalprotect-detect      (Palo Alto)
  fxf-fortios-detect            (Fortinet)
  fxf-cisco-asa-detect          (Cisco)
]]

author      = "André Henrique (@mrhenrike) | União Geek"
license     = "BSD-3-Clause"
categories  = { "discovery", "safe", "default" }

portrule = shortport.http

-- Fingerprint database: each entry has probe path, body patterns, and metadata
local FINGERPRINTS = {
    {
        vendor = "Palo Alto Networks",
        product = "PAN-OS GlobalProtect",
        paths = { "/global-protect/prelogin.esp", "/ssl-vpn/prelogin.esp" },
        patterns = { "GlobalProtect", "global%-protect", "PAN%-OS", "Palo Alto" },
        cves = { "CVE-2026-0257 (auth bypass)", "CVE-2024-3400 (cmd inject RCE)" },
        fxf_path = "exploits/perimeter/paloalto/",
    },
    {
        vendor = "Fortinet",
        product = "FortiOS",
        paths = { "/remote/login", "/api/v2/monitor/system/status" },
        patterns = { "FortiGate", "FortiOS", "Fortinet", "SSLVPN_PORTAL", "fgt_lang" },
        cves = { "CVE-2018-13379", "CVE-2022-40684", "CVE-2023-27997", "CVE-2024-21762" },
        fxf_path = "exploits/perimeter/fortinet/",
    },
    {
        vendor = "Cisco",
        product = "ASA/FTD",
        paths = { "/+CSCOE+/logon.html", "/+webvpn+/index.html" },
        patterns = { "CSCOE", "webvpn", "AnyConnect", "Firepower", "Cisco" },
        cves = { "CVE-2020-3452", "CVE-2023-20269", "CVE-2025-20362" },
        fxf_path = "exploits/perimeter/cisco/",
    },
    {
        vendor = "SonicWall",
        product = "SonicOS",
        paths = { "/auth.html", "/cgi-bin/welcome/VirtualOffice" },
        patterns = { "SonicWall", "SonicOS", "SSLVPN" },
        cves = { "CVE-2021-20034", "CVE-2024-40766", "CVE-2024-53704" },
        fxf_path = "exploits/perimeter/sonicwall/",
    },
    {
        vendor = "Sophos",
        product = "XG Firewall / SFOS",
        paths = { "/userportal/webpages/myaccount/login.jsp", "/webconsole/" },
        patterns = { "Sophos", "XG Firewall", "SFOS", "cyberoam" },
        cves = { "CVE-2020-12271 (SQLi)", "CVE-2022-1040 (auth bypass)", "CVE-2022-3236" },
        fxf_path = "exploits/perimeter/sophos/",
    },
    {
        vendor = "Check Point",
        product = "Gaia / Mobile Access",
        paths = { "/sslvpn/Login/Login", "/portal/index.html" },
        patterns = { "Check Point", "Gaia", "Mobile Access", "cpsvpnleft" },
        cves = { "CVE-2024-24919 (info disclosure)" },
        fxf_path = "exploits/perimeter/checkpoint/",
    },
    {
        vendor = "Juniper",
        product = "SRX / JunOS",
        paths = { "/", "/webauth" },
        patterns = { "Juniper", "SRX", "JunOS", "J%-Web" },
        cves = { "CVE-2023-36845 (PHP env RCE)", "CVE-2024-21591" },
        fxf_path = "exploits/perimeter/juniper/",
    },
    {
        vendor = "Zyxel",
        product = "USG/ZyWALL",
        paths = { "/cgi-bin/zysh-cgi", "/login.cgi" },
        patterns = { "Zyxel", "ZyWALL", "USG", "ZLD" },
        cves = { "CVE-2022-30525 (cmd inject)", "CVE-2023-28771 (IKE inject)" },
        fxf_path = "exploits/perimeter/zyxel/",
    },
    {
        vendor = "pfSense",
        product = "pfSense / OpenBSD",
        paths = { "/index.php", "/pfblockerng/" },
        patterns = { "pfSense", "webConfigurator", "m0n0wall" },
        cves = { "CVE-2022-31814 (pfBlockerNG RCE)", "CVE-2023-27100" },
        fxf_path = "exploits/perimeter/pfsense/",
    },
    {
        vendor = "WatchGuard",
        product = "Firebox",
        paths = { "/auth.aspx", "/api/v1/session" },
        patterns = { "WatchGuard", "Firebox", "LiveSecurity" },
        cves = { "CVE-2022-23176 (Cyclops Blink)", "CVE-2023-9.0-xcs" },
        fxf_path = "exploits/perimeter/watchguard/",
    },
    {
        vendor = "Barracuda",
        product = "Email Security Gateway",
        paths = { "/cgi-bin/index.cgi" },
        patterns = { "Barracuda", "Email Security Gateway", "ESG" },
        cves = { "CVE-2023-2868 (cmd inject)", "CVE-2023-7102" },
        fxf_path = "exploits/waf/barracuda/",
    },
}

local function try_probe(host, port, path, timeout)
    local opts = { timeout = timeout * 1000 }
    local ok, resp = pcall(http.get, host, port, path, opts)
    if not ok or not resp then return nil, nil end
    return resp.status, (resp.body or "")
end

local function score_match(body, patterns)
    local count = 0
    for _, pat in ipairs(patterns) do
        if body:find(pat) then count = count + 1 end
    end
    return count
end

action = function(host, port)
    local timeout  = tonumber(stdnse.get_script_args("fxf.timeout") or "10")
    local verbose  = stdnse.get_script_args("fxf.verbose") == "1"

    local best_match = nil
    local best_score = 0
    local best_path  = ""

    for _, fp in ipairs(FINGERPRINTS) do
        for _, path in ipairs(fp.paths) do
            local status, body = try_probe(host, port, path, timeout)
            if status and status ~= 0 and body then
                local score = score_match(body, fp.patterns)
                if score > best_score then
                    best_score = score
                    best_match = fp
                    best_path  = path
                end
            end
        end
    end

    if not best_match or best_score == 0 then return nil end

    local confidence = "LOW"
    if best_score >= 3 then confidence = "HIGH"
    elseif best_score >= 2 then confidence = "MEDIUM" end

    local results = {}
    table.insert(results, "Vendor: " .. best_match.vendor)
    table.insert(results, "Product: " .. best_match.product)
    table.insert(results, "Confidence: " .. confidence .. " (" .. best_score .. " pattern(s) matched)")
    table.insert(results, "Match path: " .. best_path)
    table.insert(results, "")
    table.insert(results, "Notable CVEs:")
    for _, cve in ipairs(best_match.cves) do
        table.insert(results, "  " .. cve)
    end
    table.insert(results, "")
    table.insert(results, "fxf modules: " .. best_match.fxf_path)
    table.insert(results, "  fxf> search " .. best_match.vendor:lower():gsub(" ", ""))

    if verbose then
        table.insert(results, "")
        table.insert(results, "Pattern score: " .. best_score .. "/" .. #best_match.patterns)
    end

    return stdnse.format_output(true, results)
end
