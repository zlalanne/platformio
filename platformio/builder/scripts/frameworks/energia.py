# Copyright (C) Ivan Kravets <me@ikravets.com>
# See LICENSE for details.

"""
Energia

Energia framework enables pretty much anyone to start easily creating
microcontroller-based projects and applications. Its easy-to-use libraries
and functions provide developers of all experience levels to start
blinking LEDs, buzzing buzzers and sensing sensors more quickly than ever
before.

http://energia.nu/reference/
"""

from os.path import join
from shutil import copytree

from SCons.Script import DefaultEnvironment

env = DefaultEnvironment()

env.Replace(
    PLATFORMFW_DIR=join("$PIOPACKAGES_DIR", "framework-energia${PLATFORM[2:]}")
)

ENERGIA_VERSION = int(
    open(join(env.subst("$PLATFORMFW_DIR"),
              "version.txt")).read().replace(".", "").strip())

# include board variants
if env.get("BOARD_OPTIONS", {}).get("build", {}).get("core") == "msp432":
    env.VariantDirWrap(
        join("$BUILD_DIR", "FrameworkEnergia"),
        join("$PLATFORMFW_DIR", "msp432", "cores", "msp432")
    )
    env.VariantDirWrap(
        join("$BUILD_DIR", "FrameworkEnergiaDriverlib"),
        join("$PLATFORMFW_DIR", "msp432", "cores", "msp432", "driverlib")
    )
    env.VariantDirWrap(
        join("$BUILD_DIR", "FrameworkEnergiaInc"),
        join("$PLATFORMFW_DIR", "msp432", "cores", "msp432", "inc")
    )
    env.VariantDirWrap(
        join("$BUILD_DIR", "Common"),
        join("$PLATFORMFW_DIR", "common")
    )
    env.VariantDirWrap(
        join("$BUILD_DIR", "CommonSrc"),
        join("$PLATFORMFW_DIR", "common", "src")
    )
    env.VariantDirWrap(
        join("$BUILD_DIR", "CommonTI"),
        join("$PLATFORMFW_DIR", "common", "xdc")
    )
    env.VariantDirWrap(
        join("$BUILD_DIR", "CMSIS"),
        join("$PLATFORMFW_DIR", "msp432", "cores", "msp432", "inc", "CMSIS")
    )
    env.Append(
        CPPPATH=[
            join("$BUILD_DIR", "FrameworkEnergiaDriverlib"),
            join("$BUILD_DIR", "FrameworkEnergiaInc"),
            join("$BUILD_DIR", "Common"),
            join("$BUILD_DIR", "CommonSrc"),
            join("$BUILD_DIR", "CommonTI"),
            join("$BUILD_DIR", "CommonXDC"),
            join("$BUILD_DIR", "CMSIS")
        ]
    )

    # include files hook

    try:
        copytree(join(env.subst("$PLATFORMFW_DIR"), "common", "gnu"),
                 join(env.subst("$BUILD_DIR"), "Common", "gnu"))
        copytree(join(env.subst("$PLATFORMFW_DIR"), "common", "configPkg"),
                 join(env.subst("$BUILD_DIR"), "Common", "configPkg"))
    except:
        pass

else:
    env.VariantDirWrap(
        join("$BUILD_DIR", "FrameworkEnergiaVariant"),
        join("$PLATFORMFW_DIR", "variants",
             "${BOARD_OPTIONS['build']['variant']}")
    )

env.Append(
    CPPDEFINES=[
        "ARDUINO=101",
        "ENERGIA=%d" % ENERGIA_VERSION
    ],
    CPPPATH=[
        join("$BUILD_DIR", "FrameworkEnergia"),
        join("$BUILD_DIR", "FrameworkEnergiaVariant")
    ]
)

if env.get("BOARD_OPTIONS", {}).get("build", {}).get("core") == "lm4f":
    env.Append(
        LINKFLAGS=["-Wl,--entry=ResetISR"]
    )

#
# Target: Build Core Library
#

libs = []

# libs.append(env.BuildLibrary(
#     join("$BUILD_DIR", "FrameworkEnergia"),
#     join("$PLATFORMFW_DIR", "msp432", "cores",
#          "${BOARD_OPTIONS['build']['core']}")
# ))

if env.get("BOARD_OPTIONS", {}).get("build", {}).get("core") == "msp432":
    env.Append(
        LIBPATH=[
            join("$PLATFORMFW_DIR", "msp432", "cores", "msp432", "driverlib"),
            join("$PLATFORMFW_DIR", "msp432", "targets",
                 "${BOARD_OPTIONS['build']['variant']}"),
            join("$PLATFORMFW_DIR", "common"),
        ]
    )


env.Append(LIBS=libs)
