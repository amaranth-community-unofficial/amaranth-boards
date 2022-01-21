import os
import subprocess

from amaranth.build import *
from amaranth.vendor.xilinx import *
from amaranth_boards.resources import *
from amaranth_boards.qmtech_daughterboard import QMTechDaughterboard

__all__ = ["QMTechXC7K325TCorePlatform"]

class QMTechXC7K325TPlatform(XilinxPlatform):
    device      = "xc7k325t"
    package     = "ffg676"
    speed       = "1"
    default_clk = "clk50"
    default_rst = "rst"

    def __init__(self, standalone=True, toolchain="ISE"):
        if not standalone:
            # we have to rename our core board LEDs/Buttons so that they don't clash
            # with the default LEDs/Buttons of the daughterboard
            self.resources[2] = Resource("core_led", 0,    PinsN("J26"), Attrs(IOSTANDARD="LVCMOS33"))
            self.resources[3] = Resource("core_led", 1,    PinsN("H26"), Attrs(IOSTANDARD="LVCMOS33"))
            self.resources[4] = Resource("core_button", 0, PinsN("AF10", dir="i"),  Attrs(IOSTANDARD="LVCMOS18"))
            daughterboard = QMTechDaughterboard(Attrs(IOSTANDARD="LVCMOS33"))
            self.connectors += daughterboard.connectors
            self.resources  += daughterboard.resources

        super().__init__(toolchain=toolchain)

    resources   = [
        Resource("clk50", 0, Pins("F22", dir="i"),
                 Clock(50e6), Attrs(IOSTANDARD="LVCMOS33")),

        # SW2
        Resource("rst", 0, PinsN("AF9", dir="i"), Attrs(IOSTANDARD="LVCMOS18")),

        *LEDResources(
            pins="J26 H26", invert=True,
            attrs=Attrs(IOSTANDARD="LVCMOS33")),

        *ButtonResources(pins="AF10", attrs=Attrs(IOSTANDARD="LVCMOS18")),

        # MT25QL128
        Resource("qspi_flash", 0,
            Subsignal("cs",        PinsN("C23")),
            Subsignal("clk",       Pins("C8")),
            Subsignal("dq",        Pins("B24 A25 B22 A22")),
            Attrs(IOSTANDARD="LVCMOS33")
        ),

        # MT41K128M16JT-125K
        Resource("ddr3", 0,
            Subsignal("rst",    PinsN("W4", dir="o"), Attrs(IOSTANDARD="LVCMOS15")),
            Subsignal("clk",    DiffPairs("AA5", "AB5", dir="o"), Attrs(IOSTANDARD="DIFF_SSTL15")),
            Subsignal("clk_en", Pins("AD1", dir="o")),
            # Subsignal("cs",   PinsN("-", dir="o")),
            Subsignal("we",     PinsN("AF4", dir="o")),
            Subsignal("ras",    PinsN("AC3", dir="o")),
            Subsignal("cas",    PinsN("AC4", dir="o")),
            Subsignal("a",      Pins("AF5 AF2 AD6 AC6 AD4 AB6 AE2 Y5 AA4 AE6 AE3 AD5 AB4 Y6", dir="o")),
            Subsignal("ba",     Pins("AD3 AE1 AE5", dir="o")),
            Subsignal("dqs",    DiffPairs("AB1 W6", "AC1 W5", dir="io"),
                                Attrs(IOSTANDARD="DIFF_SSTL15_T_DCI")),
            Subsignal("dq",     Pins("W1 V2 Y1 Y3 AC2 Y2 AB2 AA3 U1 V4 U6 W3 V6 U2 U7 U5", dir="io"),
                                Attrs(IOSTANDARD="SSTL15_T_DCI")),
            Subsignal("dm",     Pins("V1 V3", dir="o")),
            Subsignal("odt",    Pins("AF3", dir="o")),
            Attrs(IOSTANDARD="SSTL15", SLEW="FAST"),
        ),
    ]

    # The connectors are named after the daughterboard, not the core board
    # because on the different core boards the names vary, but on the
    # daughterboard they stay the same, which we need to connect the
    # daughterboard peripherals to the core board.
    # On this board J2 is U5 and J3 is U4
    connectors  = [
        Connector("J", 2, {
             # odd row     even row
             "7": "A8",    "8": "A9",
             "9": "B9",   "10": "C9",
            "11": "A10",  "12": "B10",
            "13": "D10",  "14": "E10",
            "15": "B11",  "16": "B12",
            "17": "C11",  "18": "C12",
            "19": "A12",  "20": "A13",
            "21": "D13",  "22": "D14",
            "23": "A14",  "24": "B14",
            "25": "C13",  "26": "C14",
            "27": "A15",  "28": "B15",
            "29": "D16",  "30": "D15",
            "31": "B16",  "32": "C16",
            "33": "A17",  "34": "B17",
            "35": "D18",  "36": "E18",
            "37": "C18",  "38": "C17",
            "39": "A19",  "40": "A18",
            "41": "B19",  "42": "C19",
            "43": "A20",  "44": "B20",
            "45": "D20",  "46": "D19",
            "47": "A24",  "48": "A23",
            "49": "E22",  "50": "E21",
            "51": "D24",  "52": "D23",
            "53": "D25",  "54": "E25",
            "55": "E26",  "56": "F25",
            "57": "B26",  "58": "B25",
            "59": "C26",  "60": "D26",
        }),

        Connector("J", 3, {
            # odd row     even row
             "7": "AD21",    "8": "AE21",
             "9": "AE22",   "10": "AF22",
            "11": "AE23",   "12": "AF23",
            "13": "V21",    "14": "W21",
            "15": "Y22",    "16": "AA22",
            "17": "AF24",   "18": "AF25",
            "19": "AB21",   "20": "AC21",
            "21": "AB22",   "22": "AC22",
            "23": "AD23",   "24": "AD24",
            "25": "AC23",   "26": "AC24",
            "27": "AD25",   "28": "AE25",
            "29": "AA23",   "30": "AB24",
            "31": "AA25",   "32": "AB25",
            "33": "Y23",    "34": "AA24",
            "35": "AD26",   "36": "AE26",
            "37": "AB26",   "38": "AC26",
            "39": "W23",    "40": "W24",
            "41": "Y25",    "42": "Y26",
            "43": "W25",    "44": "W26",
            "45": "U26",    "46": "V26",
            "47": "V23",    "48": "V24",
            "49": "U24",    "50": "U25",
            "51": "T22",    "52": "T23",
            "53": "R22",    "54": "R23",
            "55": "R25",    "56": "P25",
            "57": "P23",    "58": "N23",
            "59": "N26",    "60": "M26",
        })
    ]

    def toolchain_prepare(self, fragment, name, **kwargs):
        overrides = {
            "script_before_bitstream":
                "set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]",
            "script_after_bitstream":
                "write_cfgmem -force -format bin -interface spix4 -size 32 "
                "-loadbit \"up 0x0 {name}.bit\" -file {name}.bin".format(name=name),
        }
        return super().toolchain_prepare(fragment, name, **overrides, **kwargs)

    def toolchain_program(self, products, name):
        loader = os.environ.get("OPENFPGALOADER", "openFPGALoader")
        with products.extract("{}.bit".format(name)) as bitstream_filename:
            subprocess.run([loader, "-v", "-c", "ft232", bitstream_filename], check=True)


if __name__ == "__main__":
    from amaranth_boards.test.blinky import *
    QMTechXC7K325TPlatform(standalone=True).build(Blinky(), do_program=True)
