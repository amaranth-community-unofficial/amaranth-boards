import os
import subprocess

from amaranth.build import *
from amaranth.vendor.xilinx import *
from amaranth_boards.resources import *

__all__ = ["HPCXC7K420TPlatform"]

"""
Board support for this chinese Kintex 420T board by "HPC FPGA Board Store"
https://www.aliexpress.com/item/1005001631827738.html
"""
class HPCXC7K420TPlatform(XilinxPlatform):
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


    connectors  = [
        #Connector("BTB", 0, {
        #    # odd row     even row
        #    # "7": "AD21",    "8": "AE21",
        #})
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
    HPCXC7K420TPlatform().build(Blinky(), do_program=True)
