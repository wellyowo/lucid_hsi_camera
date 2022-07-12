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

from ctypes import byref

from arena_api._xlayer.xarena.arenac import harenac
from arena_api._xlayer.xarena.arenac_types import (ac_bayer_algorithm,
                                                   acBuffer, size_t, uint64_t)


class _xImagefactory():

    @staticmethod
    def xImageFactoryCreate(pdata, data_size, width, height, pixel_format):

        data_size = size_t(data_size)
        width = size_t(width)
        height = size_t(height)
        pixel_format = uint64_t(pixel_format)
        buffer = acBuffer(None)
        # AC_ERROR acImageFactoryCreate(
        #   uint8_t* pData,
        #   size_t dataSize,
        #   size_t width,
        #   size_t height,
        #   uint64_t pixelFormat,
        #   acBuffer* phDst)
        harenac.acImageFactoryCreate(
            pdata,  # will be interperted as uint8_t* correctly
            data_size,
            width,
            height,
            pixel_format,
            byref(buffer))

        return buffer.value

    @staticmethod
    def xImageFactoryCopy(hsrc):

        src_buffer = acBuffer(hsrc)
        dst_buffer = acBuffer(None)

        # AC_ERROR acImageFactoryCopy(
        #   acBuffer hSrc,
        #   acBuffer* phDst)
        harenac.acImageFactoryCopy(
            src_buffer,
            byref(dst_buffer))

        return dst_buffer.value

    @staticmethod
    def xImageFactoryDestroy(hbuffer):

        buffer = acBuffer(hbuffer)
        # AC_ERROR acImageFactoryDestroy(
        #   acBuffer hBuffer)
        harenac.acImageFactoryDestroy(
            buffer)

    @staticmethod
    def xImageFactoryConvert(hsrc_buffer, pixel_format):

        src_buffer = acBuffer(hsrc_buffer)
        pixel_format = uint64_t(pixel_format)
        dst_buffer = acBuffer(None)
        # AC_ERROR acImageFactoryConvert(
        #   acBuffer hSrc,
        #   uint64_t pixelFormat,
        #   acBuffer* phDst)
        harenac.acImageFactoryConvert(
            src_buffer,
            pixel_format,
            byref(dst_buffer))

        return dst_buffer.value

    @staticmethod
    def xImageFactoryConvertBayerAlgorithm(hsrc_buffer, pixel_format, bayer_algorithm):

        src_buffer = acBuffer(hsrc_buffer)
        pixel_format = uint64_t(pixel_format)
        bayer_algorithm = ac_bayer_algorithm(bayer_algorithm)
        dst_buffer = acBuffer(None)
        # AC_ERROR acImageFactoryConvertBayerAlgorithm(
        #   acBuffer hSrc,
        #   uint64_t pixelFormat,
        #   AC_BAYER_ALGORITHM bayerAlgo,
        #   acBuffer* phDst)
        harenac.acImageFactoryConvertBayerAlgorithm(
            src_buffer,
            pixel_format,
            bayer_algorithm,
            byref(dst_buffer))

        return dst_buffer.value
