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
- arena_api is build on the C API (ArenaC) for ArenaSDK. arena_api loads
  ArenaC binary and its dependencies automatically from ArenaSDK default
  installation directory. To load ArenaC binary from a custom location
  add the full path to ArenaC binary as a value to proper key in the dictionary.
  The dictionary name must be ``ARENAC_CUSTOM_PATHS`` and must have all of
  the following keys:

   'python32_win' :
       - used to point Python 32 on Windows to load 32 bits ArenaC binary
       - if this key has a value of empty string, arena_api loads
         '<Installation Dir>\\Win32Release\\ArenaC_v140.dll'

   'python64_win' :
       - used to point Python 64 on Windows to load 64 bits ArenaC binary
       - if this key has a value of empty string, arena_api loads
         '<Installation Dir>\\x64Release\\ArenaC_v140.dll'

   'python32_lin' :
       - used to point Python 32 on Linux to load 32 bits ArenaC binary
       - if this key has a value of empty string, arena_api uses the pathes in
         '/etc/ld.so.conf.d/Arena_SDK.conf' to find the ArenaC shared object.

   'python64_lin' :
       - used to point Python 64 on Linux to load 64 bits ArenaC binary
       - if this key has a value of empty string, arena_api uses the pathes in
         '/etc/ld.so.conf.d/Arena_SDK.conf' to find the ArenaC shared object.

 Note:
  - If the library path assigned, to any of the keys, does not
    exists a FileNotFoundError exception will rise
  - Linux keys have been tested on Ubuntu 16.04 LTS
  - To use the installed arena, give the key a value of empty string ''
  - If ArenaSDK is not installed in the default location ,
    'C:\Program Files\Lucid Vision Labs\Arena SDK', by the installer , it is
    not necessary to add the non-default installation path to the custom paths.
"""

ARENAC_CUSTOM_PATHS = {
    'python32_win': '',
    'python64_win': '',
    'python32_lin': '',
    'python64_lin': ''
}

SAVEC_CUSTOM_PATHS = {
    'python32_win': '',
    'python64_win': '',
    'python32_lin': '',
    'python64_lin': ''
}
