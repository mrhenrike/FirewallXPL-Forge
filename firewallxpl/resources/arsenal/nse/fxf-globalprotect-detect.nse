-- fxf-globalprotect-detect.nse
-- Part of FirewallXPL-Forge NSE suite.
--
-- Detects Palo Alto Networks GlobalProtect portal and gateway on the target.
-- Probes /global-protect/prelogin.esp and /ssl-vpn/prelogin.esp to fingerprint
-- the presence of GlobalProtect and extract basic metadata from the response.
--
-- Usage:
--   nmap -p 443 --script fxf-globalprotect-detect <target>
--   nmap -p 443,80,8443 --script fxf-globalprotect-detect --script-args fxf.timeout=10 <target>
--
-- Output example (vulnerable host):
--   PORT    STATE SERVICE
--   443/tcp open  https
--   | fxf-globalprotect-detect:
--   |   GlobalProtect: DETECTED
--   |   Component: portal, gateway
--   |   PAN-OS version: not disclosed
--   |_  Auth-override: check with fxf-globalprotect-auth-bypass-cve-2026-0257
--
-- Author: André Henrique (@mrhenrike) | União Geek
-- License: BSD-3-Clause

local http     = require "http"
local shortport = require "shortport"
local stdnse   = require "stdnse"
local string   = require "string"
local table    = require "table"

description = [[
Detects Palo Alto Networks GlobalProtect portal and gateway.

Sends HTTP probes to the known GlobalProtect pre-login endpoints:
  /global-protect/prelogin.esp  (portal)
  /ssl-vpn/prelogin.esp         (gateway)

Reports whether a GlobalProtect service is present and, when possible, whether
the authentication override feature is referenced in the response.
]]

author      = "André Henrique (@mrhenrike) | União Geek"
license     = "BSD-3-Clause"
categories  = { "discovery", "safe", "default" }

portrule = shortport.http

local PORTAL_PATH  = "/global-protect/prelogin.esp"
local GATEWAY_PATH = "/ssl-vpn/prelogin.esp"

local GP_PATTERNS = {
    "GlobalProtect",
    "global%-protect",
    "gp%-prelogin",
    "PAN%-OS",
    "Palo Alto Networks",
    "prelogin",
    "gateway%-version",
}

local function probe(host, port, path, timeout)
    local opts = { timeout = (timeout or 10) * 1000 }
    local response = http.get(host, port, path, opts)
    if not response or not response.body then
        return nil, nil
    end
    return response.status, response.body
end

local function detect_gp_in_body(body)
    if not body then return false end
    for _, pat in ipairs(GP_PATTERNS) do
        if body:find(pat) then return true end
    end
    return false
end

action = function(host, port)
    local timeout = tonumber(stdnse.get_script_args("fxf.timeout") or "10")
    local results = {}
    local components = {}
    local auth_override_hint = false

    local status_p, body_p = probe(host, port, PORTAL_PATH, timeout)
    if status_p and detect_gp_in_body(body_p) then
        table.insert(components, "portal")
        if body_p:find("auth%-override") or body_p:find("authentication%-override") then
            auth_override_hint = true
        end
    end

    local status_g, body_g = probe(host, port, GATEWAY_PATH, timeout)
    if status_g and detect_gp_in_body(body_g) then
        table.insert(components, "gateway")
        if body_g and (body_g:find("auth%-override") or body_g:find("authentication%-override")) then
            auth_override_hint = true
        end
    end

    if #components == 0 then
        return nil
    end

    table.insert(results, "GlobalProtect: DETECTED")
    table.insert(results, "Component: " .. table.concat(components, ", "))
    table.insert(results, "PAN-OS version: not disclosed in pre-login response")

    if auth_override_hint then
        table.insert(results, "Auth-override: referenced in response — check CVE-2026-0257 exposure")
        table.insert(results, "  Run: nmap --script fxf-globalprotect-auth-bypass-cve-2026-0257 " .. host.ip)
    else
        table.insert(results, "Auth-override: not detected in pre-login response")
        table.insert(results, "  Note: cookie may still be enabled; test with fxf CVE-2026-0257 module")
    end

    return stdnse.format_output(true, results)
end
