# -----------------------------------------------------------------------------
# Copyright (c) 2022, Lucid Vision Labs, Inc.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
# -----------------------------------------------------------------------------

from arena_api._xlayer.binary.binary import Binary
from arena_api._xlayer.binary.binary_loader import BinaryLoader
from arena_api._xlayer.xarena.arenac_configurator import ArenaCConfigurator
from arena_api.version import supported_dll_versions

_config = {
    'name': 'ArenaC',
    'name_dll': 'ArenaC_v140.dll',  # TODO check if the path validator has name checker
    'name_so': 'libarenac.so',
    # from arena_api.arena_api_config module
    'custom_pathnames_dict_name': 'ARENAC_CUSTOM_PATHS',

    # versions

    # windows
    'user_min_version_win': None,
    'user_max_version_win': None,
    'custom_build_min_version_win': (0, 0, 0, 9999),
    'custom_build_max_version_win': (0, 0, 999, 9999),
    'local_version_win': (0, 1, 0, 0),

    # linux
    'user_min_version_lin': None,
    'user_max_version_lin': None,
    'custom_build_min_version_lin': (999, 0, 0),
    'local_version_lin': (0, 1, 0),

    # arm
    'user_min_version_arm': None,
    'user_max_version_arm': None,
    'custom_build_min_version_arm': (999, 0, 0),
    'local_version_arm': (0, 1, 0),


    'dependencies_sos_lin': [
        # KEEP ORDER !!!

        # GenICam
        '../GenICam/library/lib/Linux64_x64/libGCBase_gcc54_v3_3_LUCID.so',
        '../GenICam/library/lib/Linux64_x64/libGenApi_gcc54_v3_3_LUCID.so',
        # '../GenICam/library/lib/Linux64_x64/liblog4cpp_gcc54_v3_3_LUCID.so',
        # '../GenICam/library/lib/Linux64_x64/libXmlParser_gcc54_v3_3_LUCID.so',
        # '../GenICam/library/lib/Linux64_x64/libMathParser_gcc54_v3_3_LUCID.so',
        # '../GenICam/library/lib/Linux64_x64/libLog_gcc54_v3_3_LUCID.so',
        # '../GenICam/library/lib/Linux64_x64/libNodeMapData_gcc54_v3_3_LUCID.so',

        # ArenaSDK
        'liblucidlog.so',
        'libgentl.so',
        'libarena.so'

    ],

    'dependencies_sos_arm64': [
        # KEEP ORDER !!!

        # GenICam
        '../GenICam/library/lib/Linux64_ARM/libGCBase_gcc54_v3_3_LUCID.so',
        '../GenICam/library/lib/Linux64_ARM/libGenApi_gcc54_v3_3_LUCID.so',
        # '../GenICam/library/lib/Linux64_ARM/liblog4cpp_gcc54_v3_3_LUCID.so',
        # '../GenICam/library/lib/Linux64_ARM/libMathParser_gcc54_v3_3_LUCID.so',
        # '../GenICam/library/lib/Linux64_ARM/libXmlParser_gcc54_v3_3_LUCID.so',
        # '../GenICam/library/lib/Linux64_ARM/libLog_gcc54_v3_3_LUCID.so',
        # '../GenICam/library/lib/Linux64_ARM/libNodeMapData_gcc54_v3_3_LUCID.so',
        # '../GenICam/library/lib/Linux64_ARM/libCLAllSerial_gcc54_v3_3_LUCID.so',
        # '../GenICam/library/lib/Linux64_ARM/libCLProtocol_gcc54_v3_3_LUCID.so',
        # '../GenICam/library/lib/Linux64_ARM/libFirmwareUpdate_gcc54_v3_3_LUCID.so',

        # ArenaSDK
        'liblucidlog.so',
        'libgentl.so',
        'libarena.so'

    ],

    'dependencies_sos_arm64_local': [
        # KEEP ORDER !!!

        # GenICam
        # '/mnt/c/softwarelib/GenICam//Linux64_ARM/bin/libGCBase_gcc54_v3_3_LUCID.so',
        # '/mnt/c/softwarelib/GenICam//Linux64_ARM/bin/libGenApi_gcc54_v3_3_LUCID.so',
        # '/mnt/c/softwarelib/GenICam//Linux64_ARM/bin/liblog4cpp_gcc54_v3_3_LUCID.so',
        # '/mnt/c/softwarelib/GenICam//Linux64_ARM/bin/libMathParser_gcc54_v3_3_LUCID.so',
        # '/mnt/c/softwarelib/GenICam//Linux64_ARM/bin/libXmlParser_gcc54_v3_3_LUCID.so',
        # '/mnt/c/softwarelib/GenICam//Linux64_ARM/bin/libLog_gcc54_v3_3_LUCID.so',
        # '/mnt/c/softwarelib/GenICam//Linux64_ARM/bin/libNodeMapData_gcc54_v3_3_LUCID.so',
        # '/mnt/c/softwarelib/GenICam//Linux64_ARM/bin/libCLAllSerial_gcc54_v3_3_LUCID.so',
        # '/mnt/c/softwarelib/GenICam//Linux64_ARM/bin/libCLProtocol_gcc54_v3_3_LUCID.so',
        # '/mnt/c/softwarelib/GenICam//Linux64_ARM/bin/libFirmwareUpdate_gcc54_v3_3_LUCID.so',

        # ArenaSDK
        # 'libgentld.so',
        # 'libarenad.so'

    ],

    'dependencies_sos_armhf': [
        # KEEP ORDER !!!

        # GenICam
        '../GenICam/library/lib/Linux32_ARMhf/libGCBase_gcc540_v3_3_LUCID.so',
        '../GenICam/library/lib/Linux32_ARMhf/libGenApi_gcc540_v3_3_LUCID.so',
        # '../GenICam/library/lib/Linux32_ARMhf/liblog4cpp_gcc54_v3_3_LUCID.so',
        # '../GenICam/library/lib/Linux32_ARMhf/libMathParser_gcc54_v3_3_LUCID.so',
        # '../GenICam/library/lib/Linux32_ARMhf/libXmlParser_gcc54_v3_3_LUCID.so',
        # '../GenICam/library/lib/Linux32_ARMhf/libLog_gcc54_v3_3_LUCID.so',
        # '../GenICam/library/lib/Linux32_ARMhf/libNodeMapData_gcc54_v3_3_LUCID.so',

        # ArenaSDK
        'liblucidlog.so',
        'libgentl.so',
        'libarena.so'
    ]

}


_config['user_min_version_win'] = supported_dll_versions['windows'][_config['name']]['min']
_config['user_max_version_win'] = supported_dll_versions['windows'][_config['name']]['max']

_config['user_min_version_lin'] = supported_dll_versions['linux'][_config['name']]['min']
_config['user_max_version_lin'] = supported_dll_versions['linux'][_config['name']]['max']

_config['user_min_version_arm'] = supported_dll_versions['arm'][_config['name']]['min']
_config['user_max_version_arm'] = supported_dll_versions['arm'][_config['name']]['max']


_arenac_binary = Binary(_config)
_configurator = ArenaCConfigurator(_arenac_binary.hbinary)
_configurator.configure()

harenac = _arenac_binary.hbinary
