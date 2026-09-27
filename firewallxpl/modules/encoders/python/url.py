from urllib.parse import quote

from firewallxpl.core.exploit.encoders import BaseEncoder
from firewallxpl.core.exploit.payloads import Architectures


class Encoder(BaseEncoder):
    __info__ = {
        "name": "Python URL Encoder",
        "description": "Module encodes Python payload to URL-encoded format.",
        "authors": (
            "André Henrique (@mrhenrike) | União Geek",
        ),
    }

    architecture = Architectures.PYTHON

    def encode(self, payload):
        encoded_payload = quote(payload, safe="")
        return "import urllib.parse;exec(urllib.parse.unquote('{}'))".format(encoded_payload)
