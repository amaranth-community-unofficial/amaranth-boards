import os
import subprocess

from amaranth.build import *
from amaranth.vendor.lattice_ecp5 import *
from .resources import *

from amaranth_boards.qmtech_daughterboard import QMTechDaughterboard
from amaranth_boards.colorlight_i5 import ColorLightI5Platform
from amaranth_boards.colorlight_i9 import ColorLightI9Platform

__all__ = ["ColorlightQMTechPlatform"]

"""
    This board is an adapter from the Colorlight i5/i9 SODIMM modules
    to the QMTech board form factor.
    This board is open hardware:
    https://github.com/hansfbaier/colorlight-qmtech-adapter
"""
class ColorlightQMTechPlatform(LatticeECP5Platform):
    package        = ""
    speed          = ""
    default_clk    = ""
    device         = ""
    resources      = []
    connectors     = []
    toolchain      = "Trellis"

    def __init__(self, colorlight, daughterboard=False, extra_resources=None, test=False) -> None:
        self.package        = colorlight.package
        self.speed          = colorlight.speed
        self.default_clk    = colorlight.default_clk
        self.device         = colorlight.device

        assert not (daughterboard and test), "daughterboard and test cannot be active at the same time"

        if test:
            leds = LEDResources(pins=" ".join(list(self.connectors[0].mapping.values()) + \
                                              list(self.connectors[1].mapping.values())),
                                attrs=Attrs(IO_TYPE="LVCMOS33", DRIVE="4"))

            self.resources = [colorlight.resources[0]] + leds + colorlight.resources[2:]
        elif daughterboard:
            db = QMTechDaughterboard(Attrs(IO_TYPE="LVCMOS33"))
            self.resources  = [colorlight.resources[0]] + colorlight.resources[2:] + db.resources
            self.connectors += db.connectors
        else:
            self.resources = colorlight.resources

        if extra_resources:
            self.resources += extra_resources

        super().__init__()


  # The connectors are named after the daughterboard, not the core board
    # because on the different core boards the names vary, but on the
    # daughterboard they stay the same, which we need to connect the
    # daughterboard peripherals to the core board.
    # On this board J2 is J2 and J3 is J1
    connectors = [
        Connector("J", 2, {
             # odd row     even row
              "7": "T1",    "8": "U1",
              "9": "Y2",   "10": "W1",
             "11": "V1",   "12": "M1",
             "13": "N2",   "14": "N3",
             "15": "T2",   "16": "M3",
             "17": "T3",   "18": "R3",
             "19": "N4",   "20": "M4",
             "21": "L4",   "22": "L5",
             "23": "P16",  "24": "J16",
             "25": "J18",  "26": "J17",
             "27": "H18",  "28": "H17",
             "29": "G18",  "30": "H16",
             "31": "F18",  "32": "G16",
             "33": "E18",  "34": "F17",
             "35": "F16",  "36": "E16",
             "37": "E17",  "38": "D18",
             "39": "D17",  "40": "G5",
             "41": "D16",  "42": "F5",
             "43": "E6",   "44": "E5",
             "45": "F4",   "46": "E4",
             "47": "F1",   "48": "F3",
             "49": "G3",   "50": "H3",
             "51": "H4",   "52": "H5",
             "53": "J4",   "54": "J5",
             "55": "K3",   "56": "K4",
             "57": "K5",   "58": "B3",
             "59": "A2",   "60": "B2",
        }),
        Connector("J", 3, {
            # odd row     even row
             "7": "U16",   "8": "R1",
             "9": "C18",   "10": "K18",
            "11": "R18",   "12": "T18",
            "13": "P17",   "14": "R17",
            "15": "T17",   "16": "M17",
            "17": "U17",   "18": "U18",
            "19": "N17",   "20": "P18",
            "21": "M18",   "22": "N18",
            "23": "L18",   "24": "L20",
            "25": "K19",   "26": "K20",
            "27": "J19",   "28": "J20",
            "29": "G20",   "30": "H20",
            "31": "F20",   "32": "G19",
            "33": "E20",   "34": "F19",
            "35": "D20",   "36": "E19",
            "37": "C20",   "38": "D19",
            "39": "B19",   "40": "B20",
            "41": "A19",   "42": "B18",
            "43": "A18",   "44": "C17",
            "45": "C4",    "46": "D3",
            "47": "C3",    "48": "B4",
            "49": "A3",    "50": "E3",
            "51": "B1",    "52": "C2",
            "53": "D2",    "54": "C1",
            "55": "E2",    "56": "D1",
            "57": "F2",    "58": "E1",
        })
    ]

    @property
    def required_tools(self):
        return super().required_tools + [
            "openFPGALoader"
        ]

    def toolchain_prepare(self, fragment, name, **kwargs):
        overrides = dict(ecppack_opts="--compress")
        overrides.update(kwargs)
        return super().toolchain_prepare(fragment, name, **overrides)

    def toolchain_program(self, products, name):
        tool = os.environ.get("OPENFPGALOADER", "openFPGALoader")
        with products.extract("{}.bit".format(name)) as bitstream_filename:
            subprocess.check_call([tool, '-m', bitstream_filename])

if __name__ == "__main__":
    from .test.blinky import *
    ColorlightQMTechPlatform(ColorLightI5Platform, False).build(Blinky(), do_program=True)