from firewallxpl.modules.scanners.autopwn import Exploit


class Exploit(Exploit):
    __info__ = {
        "name": "Misc Scanner",
        "description": "Module that scans for misc devices vulnerablities and weaknesses.",
        "authors": (
            "Marcin Bury <marcin[at]threat9.com>",  # firewallxpl module
        ),
        "devices": (
            "Misc Device",
        ),
    }

    modules = ["generic", "misc"]
