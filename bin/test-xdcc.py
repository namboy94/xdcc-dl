from xdcc_dl.xdcc.XDCCClient import XDCCCLient
from xdcc_dl.entities.XDCCPack import xdcc_packs_from_xdcc_message

XDCCCLient(xdcc_packs_from_xdcc_message("/msg CR-HOLLAND|NEW xdcc send #5500")[0]).download()
