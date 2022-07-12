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

from ctypes import byref, create_string_buffer, create_unicode_buffer

from arena_api._xlayer.xsave.savec import hsavec
from arena_api._xlayer.xsave.savec_types import (char_ptr, saveWriter, size_t,
                                                 uint8_t, uint64_t, wchar_ptr,
                                                 savePlyParams, bool8_t)
from arena_api._xlayer.xsave.xsave_defaults import XSAVE_STR_BUF_SIZE_DEFAULT

from arena_api._xlayer.info import Info
_info = Info()


class xWriter:
    '''
    direct mapping for c functions exclude __init__ and __del__

    '''

    def __init__(self, width=None, height=None, bits_per_pixel=None):
        self.writer = None
        self.hWriter = None

        if all([width, height, bits_per_pixel]):  # all param passed
            self.writer = self._Create(width, height, bits_per_pixel)
        elif not any([width, height, bits_per_pixel]):  # no param passed
            self.writer = self._CreateEmpty()
        else:  # some param passed
            raise ValueError('xInternal : not all args have been passed')

        self.hWriter = saveWriter(self.writer)

        # redirect functions on windows to use the Unicode SaveC function
        # WINDOWS ONLY: UNICODE handling
        # in __init__ function this function will be assigned to
        # self.SetExtension so the upper levels have on function to call
        # and the unicode for windows is handled in the __init__
        if _info.is_windows:
            self.SetExtension = self._SetExtensionU
            self.SetFileNamePattern = self._SetFileNamePatternU
            self.UpdateTag = self._UpdateTagU
            self.GetFileNamePattern = self._GetFileNamePatternU
            self.GetExtension = self._GetExtensionU
            self.PeekFileName = self._PeekFileNameU
            self.GetLastFileName = self._GetLastFileNameU

    def __del__(self):
        if self.hWriter:
            return self._Destroy()

    # only call from __init__
    @staticmethod
    def _CreateEmpty():

        hWriter = saveWriter(None)

        # SC_ERROR saveWriterCreateEmpty(
        #   saveWriter* phWriter)
        hsavec.saveWriterCreateEmpty(byref(
            hWriter))

        return hWriter.value

    # only call from __init__
    @staticmethod
    def _Create(width, height, bits_per_pixel):

        width = size_t(width)
        height = size_t(height)
        bits_per_pixel = size_t(bits_per_pixel)
        hWriter = saveWriter(None)

        # SC_ERROR saveWriterCreate(
        #   size_t width,
        #   size_t height,
        #   size_t bitsPerPixel,
        #   saveWriter* phWriter)
        hsavec.saveWriterCreate(
            width,
            height,
            bits_per_pixel,
            byref(hWriter))

        return hWriter.value

    # only call from __del__
    def _Destroy(self):

        # SC_ERROR saveWriterDestroy(
        #   saveWriter hWriter)
        hsavec.saveWriterDestroy(
            self.hWriter)

    def SetJpeg(self):

        # SC_ERROR saveWriterSetJpeg(
        #   saveWriter hWriter)
        hsavec.saveWriterSetJpeg(
            self.hWriter)

    def SetBmp(self):

        # SC_ERROR saveWriterSetBmp(
        #   saveWriter hWriter)
        hsavec.saveWriterSetBmp(
            self.hWriter)

    def SetRaw(self):

        # SC_ERROR saveWriterSetRaw(
        #   saveWriter hWriter)
        hsavec.saveWriterSetRaw(
            self.hWriter)

    def SetPly(self):

        # SC_ERROR saveWriterSetPly(
        #   saveWriter hWriter)
        hsavec.saveWriterSetPly(
            self.hWriter)

    def SetPlyAndConfigExtended(self, **kwargs):
        '''
        typedef struct savePlyParams_t
        {
            bool8_t filterPoints; /*!< Default: true. Filter NaN points (A = B = C = -32,678) */
            bool8_t isSigned;     /*!< Default: false. If true, interpret data as signed signed pixel format .Otherwise, interpret as unsigned signed pixel format  */
            float scale;          /*!< Default: 0.25f. Data scaling */
            float offsetA;        /*!< Default: 0.0f. X-axis (A) offset */
            float offsetB;        /*!< Default: 0.0f. Y-axis (B) offset */
            float offsetC;        /*!< Default: 0.0f. Z-axis (C) offset */
        } savePlyParams;
        '''
        # a hack to give it defaults
        param = savePlyParams(**savePlyParams._defaults_)
        if 'filter_points' in kwargs:
            param.filterPoints = kwargs['filter_points']

        if 'is_signed' in kwargs:
            param.isSigned = kwargs['is_signed']

        if 'scale' in kwargs:
            param.scale = kwargs['scale']

        if 'offset_a' in kwargs:
            param.offsetA = kwargs['offset_a']

        if 'offset_b' in kwargs:
            param.offsetB = kwargs['offset_b']

        if 'offset_c' in kwargs:
            param.offsetC = kwargs['offset_c']

        # SC_ERROR saveWriterSetPlyAndConfigExtended(
        #   saveWriter hWriter
        #   savePlyParams params)
        hsavec.saveWriterSetPlyAndConfigExtended(self.hWriter, param)

    def SetTiff(self):

        # SC_ERROR saveWriterSetTiff(
        #   saveWriter hWriter)
        hsavec.saveWriterSetTiff(
            self.hWriter)

    def SetPng(self):

        # SC_ERROR saveWriterSetPng(
        #   saveWriter hWriter)
        hsavec.saveWriterSetPng(
            self.hWriter)

    def SetExtension(self, extension):

        extension_p = char_ptr(extension.encode())

        # SC_ERROR saveWriterSetExtension(
        #   saveWriter hWriter,
        #   const char* pExtension)
        hsavec.saveWriterSetExtension(
            self.hWriter,
            extension_p)

    # WINDOWS ONLY: UNICODE handling
    # in __init__ function this function will be assigned to
    # self.SetExtension so the upper levels have on function to call
    # and the unicode for windows is handled in the __init__
    def _SetExtensionU(self, extension):

        extension_p = wchar_ptr(extension)

        # SC_ERROR saveWriterSetExtensionU(
        #   saveWriter hWriter,
        #   const wchar_t* pExtension)
        hsavec.saveWriterSetExtensionU(
            self.hWriter,
            extension_p)

    def SetParams(self, width, height, bits_per_pixel):

        width = size_t(width)
        height = size_t(height)
        bits_per_pixel = size_t(bits_per_pixel)

        # SC_ERROR  saveWriterSetParams(
        #   saveWriter hWriter,
        #   size_t width,
        #   size_t height,
        #   size_t bitsPerPixel)
        hsavec.saveWriterSetParams(
            self.hWriter,
            width,
            height,
            bits_per_pixel)

    def SetFileNamePattern(self, file_name_pattern):
        '''
        pattern must have an extension
        '''

        file_name_pattern_p = char_ptr(file_name_pattern.encode())

        # SC_ERROR saveWriterSetFileNamePattern(
        #   saveWriter hWriter,
        #   const char* pFileNamePattern)
        hsavec.saveWriterSetFileNamePattern(
            self.hWriter,
            file_name_pattern_p)

    # WINDOWS ONLY: UNICODE handling
    # in __init__ function this function will be assigned to
    # self.SetFileNamePattern so the upper levels have on function to call
    # and the unicode for windows is handled in the __init__
    def _SetFileNamePatternU(self, file_name_pattern):
        '''
        pattern must have an extension
        '''

        file_name_pattern_p = wchar_ptr(file_name_pattern)

        # SC_ERROR saveWriterSetFileNamePatternU(
        #   saveWriter hWriter,
        #   const wchar_t* pFileNamePattern)
        hsavec.saveWriterSetFileNamePatternU(
            self.hWriter,
            file_name_pattern_p)

    def UpdateTag(self, tag, value):

        tag_p = char_ptr(tag.encode())
        value_p = char_ptr(value.encode())

        # SC_ERROR saveWriterUpdateTag(
        #   saveWriter hWriter,
        #   const char* pTag,
        #   const char* pValue)
        hsavec.saveWriterUpdateTag(
            self.hWriter,
            tag_p, value_p)

    # WINDOWS ONLY: UNICODE handling
    # in __init__ function this function will be assigned to
    # self.UpdateTag so the upper levels have on function to call
    # and the unicode for windows is handled in the __init__
    def _UpdateTagU(self, tag, value):

        tag_p = wchar_ptr(tag)
        value_p = wchar_ptr(value)

        # SC_ERROR saveWriterUpdateTagU(
        #   saveWriter hWriter,
        #   const wchar_t* pTag,
        #   const wchar_t* pValue)
        hsavec.saveWriterUpdateTagU(
            self.hWriter,
            tag_p, value_p)

    def SetCount(self, count):

        count = uint64_t(count)

        # SC_ERROR saveWriterSetCount(
        #   saveWriter hWriter,
        #   uint64_t count)
        hsavec.saveWriterSetCount(
            self.hWriter,
            count)

    def SetCountPath(self, count):

        count = uint64_t(count)

        # SC_ERROR saveWriterSetCountPath(
        #   saveWriter hWriter,
        #   uint64_t count)
        hsavec.saveWriterSetCountPath(
            self.hWriter,
            count)

    def SetCountGlobal(self, count):

        count = uint64_t(count)

        # SC_ERROR saveWriterSetCountGlobal(
        #   saveWriter hWriter,
        #   uint64_t count)
        hsavec.saveWriterSetCountGlobal(
            self.hWriter,
            count)

    def SetTimestamp(self, timestamp):

        timestamp = uint64_t(timestamp)

        # SC_ERROR saveWriterSetTimestamp(
        #   saveWriter hWriter,
        #   uint64_t timestamp)
        hsavec.saveWriterSetTimestamp(
            self.hWriter,
            timestamp)

    def GetParams(self):

        width = size_t(0)
        height = size_t(0)
        bits_per_pixel = size_t(0)

        # SC_ERROR saveWriterGetParams(
        #   saveWriter hWriter,
        #   size_t * pWidth,
        #   size_t * pHeight,
        #   size_t * pBitsPerPixel)
        hsavec.saveWriterGetParams(
            self.hWriter,
            byref(width),
            byref(height),
            byref(bits_per_pixel))

        return width.value, height.value, bits_per_pixel.value

    def GetFileNamePattern(self):

        file_name_pattern_p = create_string_buffer(
            XSAVE_STR_BUF_SIZE_DEFAULT)
        length = size_t(XSAVE_STR_BUF_SIZE_DEFAULT)

        # SC_ERROR saveWriterGetFileNamePattern(
        #   saveWriter hWriter,
        #   char* pFileNamePattern,
        #   size_t* pLen)
        hsavec.saveWriterGetFileNamePattern(
            self.hWriter,
            file_name_pattern_p,
            byref(length))

        return file_name_pattern_p.value.decode()

    # WINDOWS ONLY: UNICODE handling
    # in __init__ function this function will be assigned to
    # self.GetFileNamePattern so the upper levels have on function to call
    # and the unicode for windows is handled in the __init__
    def _GetFileNamePatternU(self):

        file_name_pattern_p = create_unicode_buffer(
            XSAVE_STR_BUF_SIZE_DEFAULT)
        length = size_t(XSAVE_STR_BUF_SIZE_DEFAULT)

        # SC_ERROR saveWriterGetFileNamePatternU(
        #   saveWriter hWriter,
        #   wchar_t* pFileNamePattern,
        #   size_t* pLen)
        hsavec.saveWriterGetFileNamePatternU(
            self.hWriter,
            file_name_pattern_p,
            byref(length))

        return file_name_pattern_p.value

    def GetExtension(self):
        '''
        return the name with dot in the bening.
        ex:
            '.raw' not 'raw'

        '''

        extension_p = create_string_buffer(
            XSAVE_STR_BUF_SIZE_DEFAULT)
        length = size_t(XSAVE_STR_BUF_SIZE_DEFAULT)

        # SC_ERROR saveWriterGetExtension(
        #   saveWriter hWriter,
        #   char * pExtension,
        #   size_t * pLen)
        hsavec.saveWriterGetExtension(
            self.hWriter,
            extension_p,
            byref(length))

        return extension_p.value.decode()

    # WINDOWS ONLY: UNICODE handling
    # in __init__ function this function will be assigned to
    # self.GetExtension so the upper levels have on function to call
    # and the unicode for windows is handled in the __init__
    def _GetExtensionU(self):
        '''
        return the name with dot in the bening.
        ex:
            '.raw' not 'raw'

        '''

        extension_p = create_unicode_buffer(
            XSAVE_STR_BUF_SIZE_DEFAULT)
        length = size_t(XSAVE_STR_BUF_SIZE_DEFAULT)

        # SC_ERROR saveWriterGetExtensionU(
        #   saveWriter hWriter,
        #   wchar_t* pExtension,
        #   size_t* pLen)
        hsavec.saveWriterGetExtensionU(
            self.hWriter,
            extension_p,
            byref(length))

        return extension_p.value

    def PeekFileName(self):

        file_name_p = create_string_buffer(
            XSAVE_STR_BUF_SIZE_DEFAULT)
        length = size_t(XSAVE_STR_BUF_SIZE_DEFAULT)

        # SC_ERROR saveWriterPeekFileName(
        #   saveWriter hWriter,
        #   char* pFileName,
        #   size_t* pLen)
        hsavec.saveWriterPeekFileName(
            self.hWriter,
            file_name_p,
            byref(length))

        return file_name_p.value.decode()

    # WINDOWS ONLY: UNICODE handling
    # in __init__ function this function will be assigned to
    # self.PeekFileName so the upper levels have on function to call
    # and the unicode for windows is handled in the __init__
    def _PeekFileNameU(self):

        file_name_p = create_unicode_buffer(
            XSAVE_STR_BUF_SIZE_DEFAULT)
        length = size_t(XSAVE_STR_BUF_SIZE_DEFAULT)

        # SC_ERROR saveWriterPeekFileNameU(
        #   saveWriter hWriter,
        #   wchar_t* pFileName,
        #   size_t* pLen)
        hsavec.saveWriterPeekFileNameU(
            self.hWriter,
            file_name_p,
            byref(length))

        return file_name_p.value

    def PeekCount(self):

        count = uint64_t(0)

        # SC_ERROR saveWriterPeekCount(
        #   saveWriter hWriter,
        #   uint64_t* pCount)
        hsavec.saveWriterPeekCount(
            self.hWriter,
            byref(count))

        return count.value

    def PeekCountPath(self):

        count = uint64_t(0)

        # SC_ERROR saveWriterPeekCountPath(
        #   saveWriter hWriter,
        #   uint64_t* pCount)
        hsavec.saveWriterPeekCountPath(
            self.hWriter,
            byref(count))

        return count.value

    def PeekCountGlobal(self):

        count = uint64_t(0)

        # SC_ERROR saveWriterPeekCountGlobal(
        #   saveWriter hWriter,
        #   uint64_t* pCount)
        hsavec.saveWriterPeekCountGlobal(
            self.hWriter,
            byref(count))

        return count.value

    def GetLastFileName(self):
        # relative path

        file_name_p = create_string_buffer(
            XSAVE_STR_BUF_SIZE_DEFAULT)
        length = size_t(XSAVE_STR_BUF_SIZE_DEFAULT)
        # SC_ERROR saveWriterGetLastFileName(
        #   saveWriter hWriter,
        #   char* pFileName,
        #   size_t* pLen)
        hsavec.saveWriterGetLastFileName(
            self.hWriter,
            file_name_p,
            byref(length))

        return file_name_p.value.decode()

    # WINDOWS ONLY: UNICODE handling
    # in __init__ function this function will be assigned to
    # self.GetLastFileName so the upper levels have on function to call
    # and the unicode for windows is handled in the __init__
    def _GetLastFileNameU(self):
        # relative path

        file_name_p = create_unicode_buffer(
            XSAVE_STR_BUF_SIZE_DEFAULT)
        length = size_t(XSAVE_STR_BUF_SIZE_DEFAULT)
        # SC_ERROR saveWriterGetLastFileNameU(
        #   saveWriter hWriter,
        #   wchar_t* pFileName,
        #   size_t* pLen)
        hsavec.saveWriterGetLastFileNameU(
            self.hWriter,
            file_name_p,
            byref(length))

        return file_name_p.value

    def Save(self, pdata, **kwargs):

        if 'color' in kwargs:
            self._SaveWithColor(pdata, **kwargs)
        else:
            # SC_ERROR saveWriterSave(
            #   saveWriter hWriter,
            #   const uint8_t* pData)
            hsavec.saveWriterSave(
                self.hWriter,
                pdata)

    def _SaveWithColor(self, pdata, **kwargs):
        pcolor = kwargs['color']

        # because the main save pass it as true as well
        create_directories = bool8_t(True)

        # SC_ERROR saveWriterSaveWithColor(
        #   saveWriter hWriter,
        #   const uint8_t* pData,
        #   const uint8_t* pColor,
        #   bool createDirectories)
        hsavec.saveWriterSaveWithColor(
            self.hWriter,
            pdata,
            pcolor,
            create_directories)
