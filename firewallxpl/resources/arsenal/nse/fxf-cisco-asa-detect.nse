-- fxf-cisco-asa-detect.nse
-- Part of FirewallXPL-Forge NSE suite.
--
-- Detects Cisco ASA and FTD (Firepower Threat Defense) firewalls.
-- Probes the Clientless SSL-VPN portal, AnyConnect, and management interfaces.
--
-- Usage:
--   nmap -p 443,8443 --script fxf-cisco-asa-detect <target>
--
-- Output example:
--   PORT    STATE SERVICE
--   443/tcp open  https
--   | fxf-cisco-asa-detect:
--   |   Cisco ASA/FTD: DETECTED
--   |   Component: Clientless SSL-VPN, AnyConnect
--   |   Notable CVEs: CVE-2020-3452, CVE-2023-20269, CVE-2023-20198
--   |_  fxf modules: exploits/perimeter/cisco/
--
-- Author: André Henrique (@mrhenrike) | União Geek
-- License: BSD-3-Clause

local http      = require "http"
local shortport = require "shortport"
local stdnse    = require "stdnse"
local string    = require "string"
local table     = require "table"

description = [[
Detects Cisco ASA (Adaptive Security Appliance) and FTD (Firepower Threat Defense).

Probes /+CSCOE+/ and /+webvpn+/ endpoints specific to Cisco Clientless SSL-VPN,
plus AnyConnect and management paths. Reports detected components and known
CVEs exploitable via FirewallXPL-Forge.
]]

author      = "André Henrique (@mrhenrike) | União Geek"
license     = "BSD-3-Clause"
categories  = { "discovery", "safe", "default" }

portrule = shortport.http

local PROBE_PATHS = {
    { path = "/+CSCOE+/logon.html",   component = "Clientless SSL-VPN" },
    { path = "/+webvpn+/index.html",  component = "WebVPN" },
    { path = "/+CSCOE+/win.js",       component = "AnyConnect" },
    { path = "/admin/public/index.html", component = "FTD management" },
    { path = "/asa/htmlfe/logout.html", component = "ASA ASDM" },
}

local ASA_PATTERNS = {
    "CSCOE", "webvpn", "AnyConnect", "Cisco", "ASA",
    "Firepower", "FTD", "+CSCOU+",
}

local NOTABLE_CVES = {
    "CVE-2020-3452 (path traversal, CVSS 7.5)",
    "CVE-2023-20269 (VPN brute-force, CVSS 9.1)",
    "CVE-2023-20198 (IOS XE WebUI privesc, CVSS 10.0)",
    "CVE-2025-20362+20333 (FIRESTARTER chain RCE)",
}

local function is_cisco_asa(status, body, headers)
    if not status or status == 0 then return false end
    local server = ((headers or {})["server"] or "")
    if server:find("Cisco") then return true end
    if not body then return false end
    for _, pat in ipairs(ASA_PATTERNS) do
        if body:find(pat) then return true end
    end
    return false
end

action = function(host, port)
    local timeout = tonumber(stdnse.get_script_args("fxf.timeout") or "10")
    local opts = { timeout = timeout * 1000 }
    local detected = {}

    for _, probe in ipairs(PROBE_PATHS) do
        local ok, resp = pcall(http.get, host, port, probe.path, opts)
        if ok and resp and is_cisco_asa(resp.status, resp.body, resp.header) then
            table.insert(detected, probe.component)
        end
    end

    if #detected == 0 then return nil end

    local results = {}
    table.insert(results, "Cisco ASA/FTD: DETECTED")
    table.insert(results, "Component: " .. table.concat(detected, ", "))
    table.insert(results, "")
    table.insert(results, "Notable CVEs (use fxf to exploit):")
    for _, cve in ipairs(NOTABLE_CVES) do
        table.insert(results, "  " .. cve)
    end
    table.insert(results, "")
    table.insert(results, "fxf modules: exploits/perimeter/cisco/")
    table.insert(results, "  fxf> search vendor=cisco")

    return stdnse.format_output(true, results)
end
