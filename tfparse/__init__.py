# Copyright The Cloud Custodian Authors.
# SPDX-License-Identifier: Apache-2.0
import distutils.sysconfig
import json
import typing as tp
from pathlib import Path

from tfparse._tfparse import ffi


def load_lib():
    suffix = distutils.sysconfig.get_config_var("EXT_SUFFIX")

    libpath = Path(__file__).parent.parent / f"tfparse{suffix}"
    return ffi.dlopen(str(libpath))


lib = load_lib()


def load_from_path(
    filePath: bytes, stop_on_hcl_error: bool = False, debug: bool = False
) -> tp.Dict:
    s = ffi.new("char[]", filePath)
    e1 = ffi.new("int*", 1 if stop_on_hcl_error else 0)
    e2 = ffi.new("int*", 1 if debug else 0)
    ret = lib.Parse(s, e1, e2)
    ret_json = ffi.string(ret.json)
    ffi.gc(ret.json, lib.free)
    return json.loads(ret_json)