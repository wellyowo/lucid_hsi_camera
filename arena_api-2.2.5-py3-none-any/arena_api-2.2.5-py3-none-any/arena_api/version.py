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

# This dockstring block automatically gets added to docs buy copying
#  it is to docs\sphinx_docs\source\arena_api.rst in place of
#  module marker "*module_name*_module__m"
"""
- arena_api is a wrapper built on top of ArenaC library, so the package
  uses 'ArenaCd_v140.dll' or libarenac.so. The ArenaC binary has different
  versions for different platforms. Here is a way to know the minimum and
  maximum version of ArenaC supported by the current package. This could
  help in deciding whether to update arena_api or ArenaC.

>>> pprint(arena_api.version.supported_dll_versions)

- for the current platform the key 'this_platform' key can be used

>>> pprint(arena_api.version.supported_dll_versions['this_platform'])

- print loaded ArenaC and SaveC binaries versions

>>> pprint(arena_api.version.loaded_binary_versions)

"""
import subprocess

from arena_api._xlayer.info import Info as _Info

__info = _Info()


# supported_dll_versions ------------------------------------------------------


def __get_this_platform_dll_versions():

    if __info.is_windows:
        returned_dict = supported_dll_versions['windows']
    elif __info.is_arm:
        returned_dict = supported_dll_versions['arm']
    elif __info.is_linux:
        returned_dict = supported_dll_versions['linux']
    else:
        raise Exception('internal : unsupported platform')

    return returned_dict


supported_dll_versions = {
    'windows': {
        'ArenaC':
        {
            'min': (1, 0, 28, 3),
            'max': (1, 999, 999, 999),
        }
    },

    'linux': {
        'ArenaC':
        {
            'min': (0, 1, 53),
            'max': (0, 999, 999),
        }
    },
    # linux on arm
    'arm': {
        'ArenaC':
        {
            'min': (0, 1, 37),
            'max': (0, 999, 999),
        }
    },

    'this_platform': None
}
supported_dll_versions['this_platform'] = __get_this_platform_dll_versions()

# SaveC is built with ArenaC so they have the same version
for platform in supported_dll_versions.keys():
    supported_dll_versions[platform]['SaveC'] = supported_dll_versions[platform]['ArenaC']


# __version__ -----------------------------------------------------------------


def __get_version_from_pip():
    try:
        raw = subprocess.check_output(['pip', 'show', '-V', 'arena_api'],
                                      encoding='UTF-8')
    except FileNotFoundError:
        try:
            raw = subprocess.check_output(['pip3', 'show', '-V', 'arena_api'],
                                          encoding='UTF-8')
        except FileNotFoundError:
            raise Exception('arena_api requires \'pip\' to be available at '
                            'runtime to get arena_api.__version__ value. ')

    version_number = raw.split()[3]
    return version_number


__version__ = __get_version_from_pip()


# loaded_binary_versions ------------------------------------------------------

# Get ArenaC version
def __get_arenac_build_version():
    from arena_api._xlayer.xarena._xglobal import _xGlobal as _xglobal_arena

    version_str = _xglobal_arena.xGetArenaCbuildVersion()
    version_tuple = tuple()
    if version_str:
        version_int = [int(num_str) for num_str in version_str.split('.')]
        version_tuple = tuple(version_int)

    return version_tuple

# Get SaveC version
def __get_savec_build_version():
    from arena_api._xlayer.xsave._xglobal import _xGlobal as _xglobal_save

    version_str = _xglobal_save.xGetSaveСbuildVersion()
    version_tuple = tuple()
    if version_str:
        version_int = [int(num_str) for num_str in version_str.split('.')]
        version_tuple = tuple(version_int)

    return version_tuple


loaded_binary_versions = {
    'ArenaC': __get_arenac_build_version(),
    'SaveC': __get_savec_build_version()
}
