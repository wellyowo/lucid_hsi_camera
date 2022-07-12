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

from ctypes import byref, create_string_buffer

from arena_api._xlayer.xsave.savec import hsavec
from arena_api._xlayer.xsave.xsave_defaults import XSAVE_STR_BUF_SIZE_DEFAULT
from arena_api._xlayer.xsave.savec_types import size_t


class _xGlobal():

    @staticmethod
    def xGetSaveСbuildVersion():
        version_p = create_string_buffer(XSAVE_STR_BUF_SIZE_DEFAULT)
        buf_len = size_t(XSAVE_STR_BUF_SIZE_DEFAULT)

        # SC_ERROR saveGetVersion(
        #   char* pVersionBuf
        #   size_t* pBufLen)
        hsavec.saveGetVersion(
            version_p,
            byref(buf_len))

        return (version_p.value).decode()
