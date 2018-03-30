from irc.client import SimpleIRCClient
from typing import List
from xdcc_dl.entities.XDCCPack import XDCCPack
from xdcc_dl.entities.User import User
from xdcc_dl.logging.Logger import Logger


class XDCCCLient(SimpleIRCClient):
    """
    IRC Client that downloads a list of XDCC Packs
    """

    def __init__(self, packs: List[XDCCPack]):
        """
        Initializes the IRC client
        :param packs: The XDCC packs to download
        """

        self.user = User()
        self.server = packs[0].server
        self.packs = list(filter(lambda x: x.server == self.server))

        super().__init__()
