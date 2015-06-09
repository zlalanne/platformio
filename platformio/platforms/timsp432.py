# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

from platformio.platforms.base import BasePlatform


class Timsp432Platform(BasePlatform):

    """
    MSP432 microcontrollers are the ideal combination of TI's MSP430
    low-power DNA, advanced mixed-signal features, and the high performance
    processing capabilities of ARM's 32-bit Cortex M4F RISC engine.
    MSP432P4x MCUs cater to a large number of embedded applications where both
    efficient data processing and enhanced low-power operation are paramount.

    http://www.ti.com/lsds/ti/microcontrollers_16-bit_32-bit/msp/low_power_performance/msp432p4x/overview.page
    """

    PACKAGES = {

        "toolchain-gccarmnoneeabi": {
            "alias": "toolchain",
            "default": False
        },

        "tool-dslite": {
            "alias": "uploader",
            "default": False
        },

        "framework-energiamsp432": {
            "default": False
        }
    }

    def get_name(self):
        return "TI MSP432"
