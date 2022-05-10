import os
import subprocess

from amaranth.build import *
from amaranth.vendor.xilinx import *
from amaranth_boards.resources import *

__all__ = ["HPCStoreXC7K420TPlatform"]

"""
Board support for this chinese Kintex 420T board by "HPC FPGA Board Store"
https://www.aliexpress.com/item/1005001631827738.html
"""
class HPCStoreXC7K420TPlatform(XilinxPlatform):
    device      = "xc7k420t"
    package     = "ffg901"
    speed       = "2"
    default_clk = "diffclk100"
    IO_3V3      = True

    resources   = [ ]

    def get_lvcmos(self):
        return "LVCMOS33" if self.IO_3V3 else "LVCMOS25"

    def __init__(self, io_voltage="3.3V", toolchain="ISE"):
        assert io_voltage in ["2.5V", "3.3V"], "io_voltage must be '2.5V' or '3.3V' acording to the board jumper"
        if io_voltage == "2.5V":
            self.IO_3V3 = False

        self.resources += [
            Resource("clk100", 0, Pins("U24", dir="i"),
                    Clock(100e6), Attrs(IOSTANDARD=self.get_lvcmos())),

            Resource("diffclk100", 0, DiffPairs("U22", "U23", dir="i"),
                 Clock(100e6), Attrs(IOSTANDARD="LVDS_25")),

            *LEDResources(
                pins="A27 E24 G24 H21 G27 H26 H25 H24", invert=False,
                attrs=Attrs(IOSTANDARD="LVCMOS15")),

            *ButtonResources(pins="Y23 J24", invert=True, attrs=Attrs(IOSTANDARD="LVCMOS15")),

            UARTResource(0, rx="D17", tx="D16", attrs=Attrs(IOSTANDARD=self.get_lvcmos())),

            # EEPROM  AT24C04
            I2CResource(0, scl="C17", sda="C16", attrs=Attrs(IOSTANDARD=self.get_lvcmos())),

            # SODIMM located near the SFP ports
            Resource("ddr3", 0,
                Subsignal("rst",    PinsN("F27", dir="o"), Attrs(IOSTANDARD="LVCMOS15")),
                Subsignal("clk",    DiffPairs("J26", "J27", dir="o"), Attrs(IOSTANDARD="DIFF_SSTL15")),
                Subsignal("clk_en", Pins("G25", dir="o")),
                Subsignal("cs",     PinsN("H30", dir="o")),
                Subsignal("we",     PinsN("G29", dir="o")),
                Subsignal("ras",    PinsN("H27", dir="o")),
                Subsignal("cas",    PinsN("G30", dir="o")),
                Subsignal("a",      Pins("F28 E29 F26 D29 B29 C30 A30 B28 C29 B30 E30 E26 A28 H29 F25", dir="o")),
                Subsignal("ba",     Pins("F30 G28 E28", dir="o")),
                Subsignal("dqs",    DiffPairs("B18 E23 H19 K21 L23 M18 N27 N30", "A18 D23 G19 J21 K24 M19 M27 M30", dir="io"),
                                    Attrs(IOSTANDARD="DIFF_SSTL15")),
                Subsignal("dq",     Pins("A21 A22 A23 B23 B19 C19 A20 B20 C21 D21 C22 D22 E18 D18 E20 E21" + \
                                         "G18 F18 G20 F20 H20 G22 G23 F23 L18 J18 J19 K20 J22 H22 K23 J23"+ \
                                         "N24 N22 P24 P23 L20 M22 M24 N25 M17 N19 N17 P17 N20 N21 P21 P19"+ \
                                         "K26 K25 L26 L25 M25 N26 P28 P27 L30 M29 P29 R29 K28 K29 K30 M28", dir="io"),
                                    Attrs(IOSTANDARD="SSTL15")),
                Subsignal("dm",     Pins("B22 E19 F22 K19 M23 P18 P26 N29", dir="o")),
                Subsignal("odt",    Pins("J28", dir="o")),
                Attrs(IOSTANDARD="SSTL15", SLEW="FAST"),
            ),

            # SODIMM located near the power side
            Resource("ddr3", 1,
                Subsignal("rst",    PinsN("Y21", dir="o"), Attrs(IOSTANDARD="LVCMOS15")),
                Subsignal("a",      Pins("AG22 AJ23 AF22 AJ26 AG23 AD23 AF23 AJ24 AE23 AB23 AJ22 AK25 AD21 AD22 AK24", dir="o")),
                Subsignal("ba",     Pins("AK23 AF21 AC21", dir="o")),
                Subsignal("dqs",    DiffPairs("Y30 AB25 AC29 AJ27 AC17 AK19 AC16 AG14", "AA30 AC25 AC30 AJ28 AD17 AK20 AD16 AG15", dir="io"),
                                    Attrs(IOSTANDARD="DIFF_SSTL15")),
                Subsignal("dq",     Pins("W29   Y29 AB30 AB29  W28  W26  Y28 AB28 AA25 AD27 AB24 AC24  Y26  Y25 AA26 AC26" + \
                                         "AD29 AE30 AE29 AF30 AD28 AC27 AF28 AF27 AG30 AG29 AH29 AJ29 AK30 AK29 AK28 AG27" + \
                                         "AD18 AD19 AA18  Y18 AE18  Y19 AB17 AA17 AH20 AH19 AG19 AF18 AJ18 AK18 AJ17 AJ16" + \
                                         "AF16 AE16 AE15 AF15 AC15 AB15 AC14 AB14 AH17 AH16 AK14 AJ14 AF17 AG17 AH15 AH14", dir="io"),
                                    Attrs(IOSTANDARD="SSTL15")),
                Subsignal("dm",     Pins("AA28 AA27 AE28 AH30 AB18 AJ19 AD14 AK16", dir="o")),
                Subsignal("odt",    Pins("AG20", dir="o")),
                Attrs(IOSTANDARD="SSTL15", SLEW="FAST"),
            ),

            Resource("pcie", 0,
                Subsignal("rst", PinsN("W21", dir="i"), Attrs(IOSTANDARD=self.get_lvcmos())),
                Subsignal("clk", DiffPairs("T6", "T5", dir="i")),
                Subsignal("tx", DiffPairs("N4 P2 T2 V2 Y2 AB2 AD2 AF2", "N3 P1 T1 V1 Y1 AB1 AD1 AF1", dir="o")),
                Subsignal("rx", DiffPairs("P6 R4 U4 V6 W4  Y6 AA4 AB6", "P5 R3 U3 V5 W3  Y5 AA3 AB5",  dir="i")),
            ),

            Resource("sfp", 0,
                Subsignal("tx", DiffPairs("A8",  "A7", dir="o")),
                Subsignal("rx", DiffPairs("D10", "D9", dir="i")),
                Subsignal("tx_disable", PinsN("A17", dir="o"), Attrs(IOSTANDARD=self.get_lvcmos())),
                Subsignal("sda", Pins("C15", dir="io"),        Attrs(IOSTANDARD=self.get_lvcmos())),
                Subsignal("scl", Pins("A15", dir="o"),         Attrs(IOSTANDARD=self.get_lvcmos())),
            ),

            Resource("sfp", 1,
                Subsignal("tx", DiffPairs("C8",  "C7", dir="o")),
                Subsignal("rx", DiffPairs("F10", "F9", dir="i")),
                Subsignal("tx_disable", PinsN("D14", dir="o"), Attrs(IOSTANDARD=self.get_lvcmos())),
                Subsignal("sda", Pins("C14", dir="io"),        Attrs(IOSTANDARD=self.get_lvcmos())),
                Subsignal("scl", Pins("B14", dir="o"),         Attrs(IOSTANDARD=self.get_lvcmos())),
            ),

            Resource("sata", 0,
                Subsignal("tx", DiffPairs("A12", "A11", dir="o")),
                Subsignal("rx", DiffPairs("C12", "C11", dir="i")),
                Attrs(IO_TYPE="LVDS")
            ),

            Resource("sata", 1,
                Subsignal("tx", DiffPairs("B10", "B9",  dir="o")),
                Subsignal("rx", DiffPairs("E12", "E11", dir="i")),
                Attrs(IO_TYPE="LVDS")
            ),
        ]

        super().__init__(toolchain=toolchain)

    #
    #         Connector layout on the board
    #   ┌────────────────────────────────────────┐
    #   │    2                            80     │
    #   │    ┌──────────────────────────────┐    │
    #   └──┐ └──────────────────────────────┘ ┌──┘
    #      │ 1                            79  │
    #      └──────────────────────────────────┘
    #
    connectors  = [
        # Connector on the SFP side
        Connector("BTB", 0, {
          # "1":  "GND",   "2": "GND",
            "3":  "A16",   "4": "B24",
            "5":  "B17",   "6": "D24",
          # "7":  "GND",   "8": "GND",
            "9":  "E16",  "10": "A14",
            "11": "F16",  "12": "B15",
            "13": "R25",  "14": "U30",
            "15": "R24",  "16": "U29",
          # "17": "GND",  "18": "GND",
            "19": "R21",  "20": "T27",
            "21": "R20",  "22": "R26",
            "23": "T23",  "24": "U28",
            "25": "R23",  "26": "U27",
          # "27": "GND",  "28": "GND",
            "29": "T18",  "30": "V25",
            "31": "T17",  "32": "V24",
            "33": "V20",  "34": "R19",
            "35": "U20",  "36": "R18",
          # "37": "GND",  "38": "GND",
            "39": "W23",  "40": "T21",
            "41": "W22",  "42": "T20",
            "43": "U18",  "44": "V19",
            "45": "U17",  "46": "U19",
          # "47": "GND",  "48": "GND",
            "49": "T26",  "50": "W17",
            "51": "T25",  "52": "V17",
            "53": "V22",  "54": "W19",
            "55": "V21",  "56": "W18",
          # "57": "GND",  "58": "GND",
            "59": "C24",  "60": "T22",
            "61": "D26",  "62": "V30",
            "63": "C27",  "64": "U25",
            "65": "B27",  "66": "AF25",
          # "67": "GND",  "68": "GND"x
            "69": "Y24",  "70": "AH26",
            "71": "AE26", "72": "AG25",
            "73": "AD26", "74": "AH25",
          # "75": "GND",  "76": "GND"
          # "77": "NC",   "78": "3V3"
          # "79": "NC",   "80": "3V3"
        }),

        # Connector on the power side
        Connector("BTB", 1, {
          # "1":  "GND",    "2": "GND",
            "3":  "AJ11",   "4": "AK9",
            "5":  "AJ12",   "6": "AK10",
          # "7":  "GND",    "8": "GND",
            "9":  "AJ7",    "10": "AG11",
            "11": "AJ8",    "12": "AG12",
          # "13": "GND",    "14": "GND",
            "15": "AF9",    "16": "AG7",
            "17": "AF10",   "18": "AG8",
          # "19": "GND",    "20": "GND",
            "21": "AE11",   "22": "AH9",
            "23": "AE12",   "24": "AH10",
          # "25": "GND",    "26": "GND",
            "27": "AE8",    "28": "AF6",
            "29": "AE7",    "30": "AF5",
          # "31": "GND",    "32": "GND",
            "33": "AG3",    "34": "AK5",
            "35": "AG4",    "36": "AK6",
          # "37": "GND",    "38": "GND",
            "39": "AE3",    "40": "AH5",
            "41": "AE4",    "42": "AH6",
          # "43": "GND",    "44": "GND",
            "45": "AK1",    "46": "AJ3",
            "47": "AK2",    "48": "AJ4",
         #  "49": "GND",    "50": "GND",
            "51": "AC3",    "52": "AH1",
            "53": "AC4",    "54": "AH2",
          # "55": "GND",    "56": "GND",
            "57": "NC",     "58": "AC19",
            "59": "L17",    "60": "AB19",
          # "61": "GND",    "62": "GND",
            "63": "AC20",   "64": "AB20",
            "65": "AE20",   "66": "AA20",
          # "67": "GND",    "68": "GND",
            "69": "W24",    "70": "Y20",
                            "72": "AA21",
          # "73": "GND",    "74": "GND",
          # "75": "NC",     "76": "GND",
          # "77": "VCC12V", "78": "VCC3.3V",
          # "79": "VCC12V", "80": "VCC3.3V",
        }),
    ]

    def toolchain_prepare(self, fragment, name, **kwargs):
        overrides = {
            "script_before_bitstream":
                """
                set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]
                set_property BITSTREAM.GENERAL.COMPRESS TRUE [current_design]
                set_property BITSTREAM.CONFIG.CCLK_TRISTATE TRUE [current_design]
                set_property BITSTREAM.CONFIG.CONFIGRATE 66 [current_design]
                set_property CONFIG_VOLTAGE 3.3 [current_design]
                set_property CFGBVS VCCO [current_design]
                set_property BITSTREAM.CONFIG.SPI_32BIT_ADDR YES [current_design]
                set_property BITSTREAM.CONFIG.SPI_BUSWIDTH 4 [current_design]
                set_property BITSTREAM.CONFIG.SPI_FALL_EDGE YES [current_design]
                set_property BITSTREAM.CONFIG.UNUSEDPIN PULLUP [current_design]
                """,
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
    HPCStoreXC7K420TPlatform().build(Blinky(), do_program=True)
