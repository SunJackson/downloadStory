import cx_Freeze
import sys
import traceback

base = None

if sys.platform == "win32":
    base = "Win32GUI"

bdist_msi_options = {
    "upgrade_code": "{298CC832-6926-5677-F773-E71BA2B1846A}"
}

executables = [cx_Freeze.Executable("main.py",
                                    base=base,
                                    shortcutName="全网小说下载",
                      )]

cx_Freeze.setup(
    name="全网小说下载",
    options={"bdist_msi": bdist_msi_options,
             "build_exe": {"packages": ["bs4", "requests", "urllib3", "os", "sys"],
                           "includes":["sys", "os"],
                           "optimize": 2
                           }},
    version="0.1.0",
    description="全网小说下载",
    executables=executables,
    author="SunJackson"
)
