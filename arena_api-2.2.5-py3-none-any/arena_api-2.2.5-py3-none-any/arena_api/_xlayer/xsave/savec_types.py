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

import ctypes as _ctypes

'''
#    C              | ArenaC  |  Py
# signed char         int8_t
# short               int16_t   c_short
# int                 int32_t   c_int
# long long           int64_t   c_longlong
# unsigned char       uint8_t   c_ubyte
# unsigned short      uint16_t  c_ushort
# unsigned int        uint32_t  c_uint
# unsigned long long  uint64_t  c_ulonglong
# float               float     c_float
'''
# ctypes named to reflect SaveC types
bool8_t = _ctypes.c_bool

char_ptr = _ctypes.c_char_p
wchar_ptr = _ctypes.c_wchar_p
size_t = _ctypes.c_size_t


uint8_t = _ctypes.c_ubyte
uint64_t = _ctypes.c_ulonglong

double = _ctypes.c_double

saveReader = _ctypes.c_void_p
saveWriter = _ctypes.c_void_p
saveRecorder = _ctypes.c_void_p

sc_error = _ctypes.c_int


class _SavePlyParams(_ctypes.Structure):
    '''
    in SaveC
    typedef struct savePlyParams_t
    {
        bool8_t filterPoints; /*!< Default: true. Filter NaN points (A = B = C = -32,678) */
        bool8_t isSigned;	  /*!< Default: false. If true, interpret data as signed signed pixel format .Otherwise, interpret as unsigned signed pixel format  */
        float scale;		  /*!< Default: 0.25f. Data scaling */
        float offsetA;		  /*!< Default: 0.0f. X-axis (A) offset */
        float offsetB;		  /*!< Default: 0.0f. Y-axis (B) offset */
        float offsetC;		  /*!< Default: 0.0f. Z-axis (C) offset */
    } savePlyParams;

    '''
    _fields_ = [('filterPoints', _ctypes.c_bool),
                ('isSigned', _ctypes.c_bool),
                ('scale', _ctypes.c_float),
                ('offsetA', _ctypes.c_float),
                ('offsetB', _ctypes.c_float),
                ('offsetC', _ctypes.c_float)]

    _defaults_ = {'filterPoints': True,
                  'isSigned': False,
                  'scale': 0.25,
                  'offsetA': 0.0,
                  'offsetB': 0,
                  'offsetC': 0
                  }


savePlyParams = _SavePlyParams
