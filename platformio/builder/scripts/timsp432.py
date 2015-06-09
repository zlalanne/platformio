# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

"""
    Builder for TI MSP432 Series ARM microcontrollers.
"""

from os.path import join

from SCons.Script import (COMMAND_LINE_TARGETS, AlwaysBuild, Default,
                          DefaultEnvironment, SConscript)

env = DefaultEnvironment()

SConscript(env.subst(join("$PIOBUILDER_DIR", "scripts", "basearm.py")))

env.Replace(
    UPLOADER=join(
        "$PIOPACKAGES_DIR", "tool-dslite", "DebugServer", "bin", "DSLite"),
    UPLOADERFLAGS=[
        "-c", join("$PIOPACKAGES_DIR", "tool-dslite", "MSP432P401R.ccxml"),
        "-f"
    ],

    UPLOADCMD="$UPLOADER $UPLOADERFLAGS $SOURCES"
)


env.Append(
    CPPDEFINES=[
        "xdc__nolocalstring=1",
        "xdc_target_types__=\"gnu/targets/arm/std.h\"",
        "xdc_target_name__=M4F",
        'xdc_cfg__xheader__="<configPkg/package/cfg/energia_pm4fg.h>"'
    ],

    CPPFLAGS=[
        "-mfloat-abi=hard",
        "-mfpu=fpv4-sp-d16",
        "-fsingle-precision-constant",
        "-mabi=aapcs"
    ],

    LIBS=["stdc++", "nosys"],

    LINKFLAGS=[
        "-nostartfiles",
        "-Wl,--no-wchar-size-warning",
        "-Wl,-static",
        "-mfloat-abi=hard",
        "-mfpu=fpv4-sp-d16"
    ]
)

#
# Target: Build executable and linkable firmware
#

target_elf = env.BuildFirmware()

#
# Target: Build the .bin file
#

if "uploadlazy" in COMMAND_LINE_TARGETS:
    target_firm = join("$BUILD_DIR", "firmware.bin")
else:
    target_firm = env.ElfToBin(join("$BUILD_DIR", "firmware"), target_elf)

#
# Target: Print binary size
#

target_size = env.Alias("size", target_elf, "$SIZEPRINTCMD")
AlwaysBuild(target_size)

#
# Target: Upload by default .elf file
#

upload = env.Alias(["upload", "uploadlazy"], target_elf, "$UPLOADCMD")
AlwaysBuild(upload)

#
# Target: Define targets
#

Default([target_firm, target_size])
