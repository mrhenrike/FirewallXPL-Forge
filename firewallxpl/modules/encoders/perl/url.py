from urllib.parse import quote

from firewallxpl.core.exploit.encoders import BaseEncoder
from firewallxpl.core.exploit.payloads import Architectures


class Encoder(BaseEncoder):
    __info__ = {
        "name": "Perl URL Encoder",
        "description": "Module encodes PERL payload to URL-encoded format.",
        "authors": (
            "André Henrique (@mrhenrike) | União Geek",  # FirewallXPL-Forge encoder
        ),
    }

    architecture = Architectures.PERL

    def encode(self, payload):
        encoded_payload = quote(payload, safe="")
        return "use URI::Escape;eval(uri_unescape('{}'));".format(encoded_payload)
