import inspect
import os
import queue
import re
import threading
from pathlib import Path

from arena_api._xlayer.xsave.xrecorder import xRecorder as _xRecorder
from arena_api._xlayer.xsave.xwriter import xWriter as _xWriter
from arena_api.buffer import BufferFactory
from arena_api.enums import PixelFormat


# TODO add enums


class _FileNamePatternManager:
    def __init__(self):
        self.pattern = None
        self.tags = {}
        self.supported_extensions = None

    def register_tag(self, name, generator):
        self.tags[name] = {'generator': generator}

    def evaluate_pattern(self):
        temp = self.pattern
        for tag, value in self.tags.items():
            generator = value['generator']
            next_val = next(generator)
            next_val_str = str(next_val)
            temp = temp.replace(f'<{tag}>', next_val_str)
        return temp

    @staticmethod
    def get_tags_in_str(pattern):
        # TODO
        # - handle:
        #   !allowed :
        #       <1>, <1e>, <#dd>, <1e1>
        #   allowed :
        #       <e>,, <e1>, <e1e>
        #
        # handled:
        #   !allowed :
        #
        #   allowed :
        #       - <    e  >  -->  <\s*(
        #
        groups = re.findall('(<(\w+)>)+', pattern)
        tags = set()
        for group in groups:
            # getting the second captured group
            tags.add(group[1].strip())
        return tags

    # VALIDATORS --------------------------------------------------------------

    def raise_if_unregistered_tag(self, tags):
        for tag in tags:
            if tag not in self.tags:
                raise ValueError(f'\'{tag}\' is not a registered tag. Use '
                                 f'\'register_tag()\' to register a '
                                 f'tag.')

    def raise_if_unsupported_extension(self, pattern):
        """
        - savec will return error if pattern did not have a file extension.
        - supports one dont extension only
        """
        pathname = Path(pattern)
        extension = pathname.suffix  # could be multiple extensions
        # unsupported extension
        if extension.lower() not in self.supported_extensions:
            # TODO investigate
            # suggested by warn to add the jfi extension at the end
            # print(extension)
            # extension = f'{extension}.lol' # update extension
            # print(extension)

            if not extension:
                raise ValueError(f'provide extension to name pattern')

            raise ValueError(f'\'{extension}\' file extension is '
                             f'not supported')


class Writer:
    """
    settable
    - limited set
        - width
        - height
        - bits_per_pixel
        - ? supported extensions?
    - settable
       - tag
       - pattern
       - output_dir
       - last saved # TODO
       - next? might be problematic with generators
    # TODO
    - add a more tags and the all are from buffer for buffer
    - fix <><> regex pattern
    - documentations
    - a way to get the class infos as non settable values
    - give access to generator function inside the class
    - flag to confirm saving
    - all attrs can be set from __init__
    - implements __repr__
    - pixel format ->file format map validation?
    - ? rename pattern to filename_pattern ?
    """

    def __init__(self, width=None, height=None, bits_per_pixel=None):
        self._pattern_mngr = None
        self._xwriter = None
        self._params_were_passed = None
        self.config = None
        self._output_dir = None
        self._saved_images = []
        # hold prev pattern in case a new tamp pattern is passed for save() to
        # save on image then back to the main pattern
        self._old_pattern = None

        # pattern -------------------------------------------------------------

        # sets default pattern
        self._pattern_mngr = _FileNamePatternManager()
        self._pattern_mngr.supported_extensions = (
            '.jpeg',  '.jpg', '.bmp', '.raw', '.ply', '.tiff', '.png')

        # args ----------------------------------------------------------------

        if all([width, height, bits_per_pixel]):  # all param passed
            self._xwriter = _xWriter(width, height, bits_per_pixel)
            self._params_were_passed = True

        elif not any([width, height, bits_per_pixel]):  # no param passed
            self._xwriter = _xWriter()
            self._params_were_passed = False
        else:  # some param passed
            raise ValueError('Internal : not all args have been passed')

        # config --------------------------------------------------------------

        self.config = {'width': width,
                       'height': height,
                       'bits_per_pixel': bits_per_pixel,
                       'tags': self._pattern_mngr.tags}

        # others --------------------------------------------------------------

        # default tags
        def update_count():
            count = 0
            while True:
                yield count
                count += 1
        self.register_tag('count', update_count())

        # default pattern
        self.pattern = 'image_<count>.jpg'

    @classmethod
    def from_buffer(cls, buffer):
        return cls(buffer.width, buffer.height, buffer.bits_per_pixel)

    # tag ---------------------------------------------------------------------

    def register_tag(self, name, generator):

        # is a generator function or
        if not inspect.isgenerator(generator) and\
                not inspect.isgeneratorfunction(generator):
            raise TypeError(f'Expected a GeneratorType instead '
                            f'of {type(generator)}')

        self._pattern_mngr.register_tag(name, generator)

    def deregister_tag(self, name):
        del self.config['tag'][name]

    # pattern -----------------------------------------------------------------

    def __get_pattern(self):
        return self._pattern_mngr.pattern

    def __set_pattern(self, pattern):
        # tags
        input_tags = self._pattern_mngr.get_tags_in_str(pattern)
        self._pattern_mngr.raise_if_unregistered_tag(input_tags)

        # extension
        self._pattern_mngr.raise_if_unsupported_extension(pattern)

        # accepted pattern
        self._pattern_mngr.pattern = pattern

    pattern = property(__get_pattern, __set_pattern)

    # output_dir --------------------------------------------------------------

    def __get_output_dir(self):
        return str(self._output_dir)

    def __set_output_dir(self, output_dir):
        self._output_dir = Path(output_dir)

    output_dir = property(__get_output_dir, __set_output_dir)

    # saved images ------------------------------------------------------------

    def __get_saved_images(self):
        # so users don't change the saved images so far
        return tuple(self._saved_images)

    saved_images = property(__get_saved_images)

    # save --------------------------------------------------------------------

    def save(self, buffer, pattern=None, **kwargs):

        # TODO check if the width and height has changed

        # args ----------------------------------------------------------------

        # self
        # check if the writer is ready
        # TODO what if user want to change width and height and bits
        if not self._params_were_passed:
            self._xwriter.SetParams(buffer.width,
                                    buffer.height,
                                    buffer.bits_per_pixel)
            self.config['width'] = buffer.width
            self.config['height'] = buffer.height
            self.config['bits_per_pixel'] = buffer.bits_per_pixel
            self._params_were_passed = True

        # buffer --------------------------------------------------------------

        # TODO is savable pixel format check

        # name ----------------------------------------------------------------

        # default name is already set
        # update pattern to new name
        if pattern and pattern != self.pattern:
            self._old_pattern = self.pattern
            self.pattern = pattern
        elif not pattern and self._old_pattern:
            self.pattern = self._old_pattern
            self._old_pattern = None

        # file name that will be saved with
        updated_name = self._pattern_mngr.evaluate_pattern()

        # if the output dir is not the working dir
        if self._output_dir:
            updated_name = str(self._output_dir / updated_name)

        # TODO
        # FIXME if pattern passed is "hi.jpg" the GetExtension() returns "".jp"
        # STEPS TO REPRODUCE
        # print(self._xwriter.GetExtension())
        # self.buffer = buffer
        # self._xwriter.SetFileNamePattern(updated_name)
        # print(self._xwriter.GetExtension())

        # sent name
        self._xwriter.SetFileNamePattern(updated_name)

        # point cloud buffer ?
        # resets after saving
        is_ply = Path(updated_name).suffix == '.ply'
        if is_ply:
            # check if more args is passed
            self._xwriter.SetPlyAndConfigExtended(**kwargs)

        # save ----------------------------------------------------------------
        if is_ply:
            self._xwriter.Save(buffer.pdata, **kwargs)
        else:
            self._xwriter.Save(buffer.pdata)

        # attach current working dir to the image name because the
        # SaveC returns a relative name
        if not self._output_dir:
            # TODO might be good to save it in a private_var
            updated_name = str(Path(os.getcwd()) / updated_name)
        self._saved_images.append(updated_name)

        # TODO validate that it was written to dir

        # self.buffer = None
        # del self.buffer

    def __repr__(self):
        pass


class Recorder:

    def __init__(self,
                 width=None,
                 height=None,
                 frames_per_second=None,
                 threaded=None):

        print(f'save.Recorder class is an alpha release and is still '
              f'under development. Please do not use in production as if yet!')
        # TODO number of images to top at
        self.is_threaded = threaded
        self._pattern_mngr = None
        self._xrecorder = None
        self._params_were_passed = None
        self.config = None
        self._output_dir = None
        self._saved_videos = []
        self.append = self._append  # append function

        # threading ----------------------------------------------------------
        if self.is_threaded:
            # Only Recorder.Open() changes it to True and
            # Only Recorder.close() changes it to False
            self._run = threading.Event()

            self._thread = None
            self._queue = queue.Queue()

            self.append = self._append_threaded  # append function but threaded

        # pattern -------------------------------------------------------------

        # sets default pattern
        self._pattern_mngr = _FileNamePatternManager()
        self._pattern_mngr.supported_extensions = ('.mp4',)

        # args ----------------------------------------------------------------

        if all([width, height, frames_per_second]):  # all param passed
            self._xrecorder = _xRecorder(width, height, frames_per_second)
            self._params_were_passed = True

        elif not any([width, height, frames_per_second]):  # no param passed
            self._xrecorder = _xRecorder()
            self._params_were_passed = False
        else:  # some param passed
            raise ValueError('Internal : not all args have been passed')

        # config --------------------------------------------------------------

        self.config = {'width': width,
                       'height': height,
                       'fps': frames_per_second,
                       'tags': self._pattern_mngr.tags}

        # codec ---------------------------------------------------------------
        self._supported_codec = {
            # ('raw'): None,
            frozenset(('raw', 'avi', 'bgr8')): self._xrecorder.SetRawAviBGR8,
            frozenset(('raw', 'mov', 'rgb8')): self._xrecorder.SetRawMovRGB8,
            frozenset(('h264', 'mov', 'rgb8')): self._xrecorder.SetH264MovRGB8,
            frozenset(('h264', 'mov', 'bgr8')): self._xrecorder.SetH264MovBGR8,
            frozenset(('h264', 'mp4', 'rgb8')): self._xrecorder.SetH264Mp4RGB8,
            frozenset(('h264', 'mp4', 'bgr8')): self._xrecorder.SetH264Mp4BGR8,
            # TODO IMPROVE maybe remove it to attr
            '_current': None,
        }

        # others --------------------------------------------------------------

        # default tags

        def update_count():
            count = 0
            while True:
                yield count
                count += 1
        self.register_tag('count', update_count())

        # default pattern
        self.pattern = 'video_<count>.mp4'

    #
    # tag -----------------------------------------------------------------
    #

    def register_tag(self, name, generator):

        # is a generator function or
        if not inspect.isgenerator(generator) and\
                not inspect.isgeneratorfunction(generator):
            raise TypeError(f'Expected a GeneratorType instead '
                            f'of {type(generator)}')

        self._pattern_mngr.register_tag(name, generator)

    def deregister_tag(self, name):
        del self.config['tag'][name]

    #
    # pattern -----------------------------------------------------------------
    #

    def __get_pattern(self):
        return self._pattern_mngr.pattern

    def __set_pattern(self, pattern):
        # tags
        input_tags = self._pattern_mngr.get_tags_in_str(pattern)
        self._pattern_mngr.raise_if_unregistered_tag(input_tags)

        # extension
        self._pattern_mngr.raise_if_unsupported_extension(pattern)

        # accepted pattern
        self._pattern_mngr.pattern = pattern

    pattern = property(__get_pattern, __set_pattern)

    #
    # output_dir --------------------------------------------------------------
    #

    def __get_output_dir(self):
        return str(self._output_dir)

    def __set_output_dir(self, output_dir):
        self._output_dir = Path(output_dir)

    output_dir = property(__get_output_dir, __set_output_dir)

    #
    # saved videos ------------------------------------------------------------
    #

    def __get_saved_videos(self):
        # so users dont change the saved videos so far
        return tuple(self._saved_videos)

    saved_videos = property(__get_saved_videos)

    #
    # codec -------------------------------------------------------------------
    #

    def __get_codec(self):
        return self._supported_codec['_current']

    def __set_codec(self, set_of_codec_container_pixelformat):

        # TODO need a better way
        try:
            set_of_codec_container_pixelformat = frozenset(
                set_of_codec_container_pixelformat)
            setter_func = self._supported_codec[set_of_codec_container_pixelformat]
            self._supported_codec['_current'] = set_of_codec_container_pixelformat
        except KeyError:
            raise ValueError(
                f'{set_of_codec_container_pixelformat} is not supported '
                f'combination of codec, container, and pixel format')

        setter_func()
    codec = property(__get_codec, __set_codec)

    def __repr__(self):
        pass

    #
    # open / close ------------------------------------------------------------
    #

    # TODO make as context manger
    def open(self, width=None, height=None, frames_per_second=None):
        """
        """

        # args ----------------------------------------------------------------
        # check if the writer is ready

        if not self._params_were_passed:
            if all([width, height, frames_per_second]):  # all param passed
                self._xrecorder.SetParams(width, height, frames_per_second)
                self._params_were_passed = True
            elif not any([width, height, frames_per_second]):  # no param passed
                raise ValueError(
                    'Set \'width\' and \'height\' before opening recorder')  # fsp not important ?
            else:  # some param passed
                # fsp not important ?
                raise ValueError(
                    'Set \'width\' and \'height\' before opening recorder')

        # Other vars
        # example :(h264 , extension , pixelformat)
        # TODO improve this (pixelformat upper case)
        codec_as_list = sorted(list(self.codec))
        pixel_format = codec_as_list[0]
        self._video_pixel_format = PixelFormat[pixel_format.upper()]

        # name ----------------------------------------------------------------

        # file name that will be saved with
        updated_name = self._pattern_mngr.evaluate_pattern()

        # if the output dir is not the working dir
        if self._output_dir:
            updated_name = str(self._output_dir / updated_name)

        self._xrecorder.SetFileNamePattern(updated_name)

        # Threading -----------------------------------------------------------
        # this function runs one so it is ok to have it handle both threaded
        # and single-threaded
        if self.is_threaded:
            self._thread = threading.Thread(
                target=self._convert_and_append_buffer_thread)
            self._run.set()
            self._thread.start()

        # TODO update the config
        self._xrecorder.Open()

    def close(self):
        """
        """
        # this function runs once so it is ok for it to handle
        # both threaded and single threading
        if self.is_threaded:
            # queue ---------------------------------------------------------------
            # will mark to the second thread that
            # the last item has been pushed
            self._queue.put(None)

            # event ---------------------------------------------------------------
            # for starting to record again
            self._run.clear()

            # thread --------------------------------------------------------------
            self._thread.join()

        # xlayer --------------------------------------------------------------
        self._xrecorder.Close()
        updated_name = self._xrecorder.GetFileNamePattern()

        # last_file_path ------------------------------------------------------
        # attach current working dir to the file name because the
        # SaveC returns a relative name
        if not self._output_dir:
            # TODO might be good to save it in a private_var
            updated_name = str(Path(os.getcwd()) / updated_name)
        self._saved_videos.append(updated_name)

        # TODO validate that it was written to dir

    #
    # append ------------------------------------------------------------------
    #

    def _append_threaded(self, buffer):
        # the second thread of conversion and append is
        # calling ``BufferFactory.destroy()`` on
        # copied buffers
        cp_buffer = BufferFactory.copy(buffer)
        self._queue.put(cp_buffer)  # thread safe if queue.empty() is not used

    def _append(self, buffer):

        # TODO check of conv is needed
        conv_buffer = BufferFactory.convert(buffer, self._video_pixel_format)

        # add to the video
        self._xrecorder.AppendImage(conv_buffer.pdata)

        # free memory
        # release the copied and converted buffer image
        BufferFactory.destroy(conv_buffer)

    #
    # Others ------------------------------------------------------------------
    #

    def _convert_and_append_buffer_thread(self):
        # wait for open() to set the run var
        self._run.wait()

        while True:
            # buffers
            cp_buffer = self._queue.get()
            if not cp_buffer:
                break

            # convert
            # TODO check if needed might have the same pixel format
            conv_buffer = BufferFactory.convert(cp_buffer,
                                                self._video_pixel_format)

            # add to the video
            self._xrecorder.AppendImage(conv_buffer.pdata)

            # free memory
            # release the copied and converted buffer image
            BufferFactory.destroy(cp_buffer)
            BufferFactory.destroy(conv_buffer)

            self._queue.task_done()
