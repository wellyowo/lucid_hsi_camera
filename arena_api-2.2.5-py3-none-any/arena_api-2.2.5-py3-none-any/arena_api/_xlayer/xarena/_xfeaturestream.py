
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
from arena_api._xlayer.xarena.arenac_types import (acFeatureStream, acNodeMap,
                                                   char_ptr)


class _xFeaturestream():

    def __init__(self, ac_nodemap_address):
        # TODO SFW-2546
        if not ac_nodemap_address:
            raise TypeError('ac_nodemap_address is None')

        self.ac_featurestream_address = self._xFeatureStreamCreate(
            ac_nodemap_address)
        self.ac_featurestream = acFeatureStream(self.ac_featurestream_address)

    def __del__(self):
        self._xFeatureStreamDestroy()

    def _xFeatureStreamCreate(self, ac_nodemap_address):
        ac_nodemap = acNodeMap(ac_nodemap_address)
        ac_featurestream = acFeatureStream(None)
        # AC_ERROR acFeatureStreamCreate(
        #   acNodeMap hNodeMap,
        #   acFeatureStream* phFeatureStream)
        harenac.acFeatureStreamCreate(
            ac_nodemap,
            byref(ac_featurestream))

        return ac_featurestream.value

    def _xFeatureStreamDestroy(self):
        # AC_ERROR acFeatureStreamDestroy(
        #   acFeatureStream hFeatureStream)
        harenac.acFeatureStreamDestroy(
            self.ac_featurestream)

    def xFeatureStreamSelect(self, feature_name):

        feature_name_p = char_ptr(feature_name.encode())
        # AC_ERROR acFeatureStreamSelect(
        #   acFeatureStream hFeatureStream,
        #   char* pFeatureName)
        harenac.acFeatureStreamSelect(
            self.ac_featurestream,
            feature_name_p)

    def xFeatureStreamWrite(self):

        # AC_ERROR acFeatureStreamWrite(
        #   acFeatureStream hFeatureStream)
        harenac.acFeatureStreamWrite(
            self.ac_featurestream)

    def xFeatureStreamWriteFileName(self, file_name):

        file_name_p = char_ptr(file_name.encode())
        # AC_ERROR acFeatureStreamWriteFileName(
        #   acFeatureStream hFeatureStream,
        #   char* pFileName)
        harenac.acFeatureStreamWriteFileName(
            self.ac_featurestream,
            file_name_p)

    def xFeatureStreamRead(self):

        # AC_ERROR acFeatureStreamRead(
        #   acFeatureStream hFeatureStream)
        harenac.acFeatureStreamRead(
            self.ac_featurestream)

    def xFeatureStreamReadFileName(self, file_name):

        file_name_p = char_ptr(file_name.encode())
        # AC_ERROR acFeatureStreamReadFileName(
        #   acFeatureStream hFeatureStream,
        #   char* pFileName)
        harenac.acFeatureStreamReadFileName(
            self.ac_featurestream,
            file_name_p)
