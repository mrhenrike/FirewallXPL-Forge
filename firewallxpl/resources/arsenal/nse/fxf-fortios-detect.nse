-- fxf-fortios-detect.nse
-- Part of FirewallXPL-Forge NSE suite.
--
-- Detects Fortinet FortiOS SSL-VPN and FortiGate management interfaces.
-- Probes known paths and examines HTTP headers/body for FortiOS fingerprints.
--
-- Usage:
--   nmap -p 443,10443,8443 --script fxf-fortios-detect <target>
--   nmap -p 443 --script fxf-fortios-detect --script-args fxf.timeout=15 <target>
--
-- Output example:
--   PORT    STATE SERVICE
--   443/tcp open  https
--   | fxf-fortios-detect:
--   |   FortiOS: DETECTED
--   |   Component: SSL-VPN portal
--   |   Server header: FortiHTTP
--   |   Notable CVEs: CVE-2018-13379, CVE-2022-40684, CVE-2023-27997, CVE-2024-21762
--   |_  Use fxf module: exploits/perimeter/fortinet/
--
-- Author: André Henrique (@mrhenrike) | União Geek
-- License: BSD-3-Clause

local http      = require "http"
local shortport = require "shortport"
local stdnse    = require "stdnse"
local string    = require "string"
local table     = require "table"

description = [[
Detects Fortinet FortiOS / FortiGate firewalls and SSL-VPN portals.

Probes common management and SSL-VPN endpoints for FortiOS-specific HTTP responses,
Server headers, and HTML content. Reports detected components and relevant CVE
modules available in FirewallXPL-Forge.
]]

author      = "André Henrique (@mrhenrike) | União Geek"
license     = "BSD-3-Clause"
categories  = { "discovery", "safe", "default" }

portrule = shortport.http

local PROBE_PATHS = {
    { path = "/remote/login",      component = "SSL-VPN portal" },
    { path = "/login",             component = "Management interface" },
    { path = "/api/v2/monitor/system/status", component = "REST API (unauthenticated probe)" },
    { path = "/remote/fgt_lang",   component = "SSL-VPN language file" },
}

local FORTI_PATTERNS = {
    "FortiGate", "FortiOS", "Fortinet", "fortigate", "fortios",
    "fgt_lang", "remote/login", "SSLVPN_PORTAL",
}

local NOTABLE_CVES = {
    "CVE-2018-13379 (path traversal, CVSS 9.8)",
    "CVE-2022-40684 (auth bypass, CVSS 9.8)",
    "CVE-2023-27997 (SSL-VPN heap RCE, CVSS 9.8)",
    "CVE-2024-21762 (SSL-VPN OOB write RCE, CVSS 9.6)",
    "CVE-2024-55591 (WebSocket auth bypass, CVSS 9.8)",
}

local function is_forti(status, body, headers)
    if not status or status == 0 then return false end
    local server = (headers and headers["server"]) or ""
    if server:find("FortiHTTP") or server:find("Fortinet") then return true end
    if not body then return false end
    for _, pat in ipairs(FORTI_PATTERNS) do
        if body:find(pat) then return true end
    end
    return false
end

action = function(host, port)
    local timeout = tonumber(stdnse.get_script_args("fxf.timeout") or "10")
    local opts = { timeout = timeout * 1000 }
    local detected = {}
    local server_header = ""

    for _, probe in ipairs(PROBE_PATHS) do
        local ok, resp = pcall(http.get, host, port, probe.path, opts)
        if ok and resp then
            local hdrs = resp.header or {}
            local srv = (hdrs["server"] or hdrs["Server"] or "")
            if srv ~= "" and server_header == "" then server_header = srv end
            if is_forti(resp.status, resp.body, hdrs) then
                table.insert(detected, probe.component)
            end
        end
    end

    if #detected == 0 then return nil end

    local results = {}
    table.insert(results, "FortiOS: DETECTED")
    table.insert(results, "Component: " .. table.concat(detected, ", "))
    if server_header ~= "" then
        table.insert(results, "Server header: " .. server_header)
    end
    table.insert(results, "")
    table.insert(results, "Notable CVEs (use fxf to exploit):")
    for _, cve in ipairs(NOTABLE_CVES) do
        table.insert(results, "  " .. cve)
    end
    table.insert(results, "")
    table.insert(results, "fxf modules: exploits/perimeter/fortinet/")
    table.insert(results, "  fxf> search vendor=fortinet")

    return stdnse.format_output(true, results)
end
