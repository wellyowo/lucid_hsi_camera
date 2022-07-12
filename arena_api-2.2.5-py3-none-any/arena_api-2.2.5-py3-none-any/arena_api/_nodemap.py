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

import difflib

from arena_api import _node_helpers, _node
from arena_api._xlayer.xarena._xnodemap import _xNodemap
from arena_api._xlayer.xarena._xfeaturestream import _xFeaturestream


class Nodemap():
    """
    only ``arena_api`` instantiates this class.
    use print function to get a list of all feature nodes under
    a nodemap instance.
    """
    # TODO SFW-2115

    def __init__(self, xhnodemap):
        self.__xnodemap = _xNodemap(xhnodemap)
        self.DEFAULT_POLL_TIME_MILLISEC = 1000
        self._nodemap_type_name = 'default_name_nodemap'

    def __repr__(self):
        return str(self.feature_names)
        pass
    # device_name ---------------------------------------------------------

    def __get_device_name(self):
        return self.__xnodemap.xNodeMapGetDeviceName()

    device_name = property(__get_device_name)
    """
    Name of the device which the node map is comming from.

    :getter: returns the device name
    :type: ``str``

    **--------------------------------------------------------------**\
    **---------------------------------------------------------------**

    """

    # ---------------------------------------------------------------------

    def invalidate_nodes(self):
        """
        **--------------------------------------------------------------**\
        **---------------------------------------------------------------**
        """
        self.__xnodemap.xNodeMapInvalidateNodes()

    def __check_poll_parameter_elapsed_time_millisec(self, elapsed_time_millisec):
        # check types
        if elapsed_time_millisec is None:
            elapsed_time_millisec = self.DEFAULT_POLL_TIME_MILLISEC

        if not isinstance(elapsed_time_millisec, int):
            raise TypeError(f'expected int instead of '
                            f'{type(elapsed_time_millisec).__name__}')

        if elapsed_time_millisec <= 0:
            raise ValueError('timeout must be > 0')

        return elapsed_time_millisec

    def poll(self, elapsed_time_millisec=None):
        # TODO SFW-2286
        """
        **Args**:\n
            elapsed_time_millisec: can be\n
            - a positive ``int`` value that represents\
            the delta of time, in millisec, to poll. \
            The value zero causes ``ValueError`` to rise.\n
            - ``None``. This is the parameter's default value. The\
            function will use ``nodemap.DEFAULT_POLL_TIME_MILLISEC``\
            value instead --which has a default value of ``1000``.\n
        **Raises**:\n
        - ``ValueError``:\n
            - elapsed_time_millisec is ``0``.
        - ``TypeError``:\n
                - elapsed_time_millisec type is not ``int``, nor ``None``.

        **Returns**:
            - ``None``.\n
        **--------------------------------------------------------------**\
        **---------------------------------------------------------------**
        """

        elapsed_time_millisec = (
            self.__check_poll_parameter_elapsed_time_millisec(
                elapsed_time_millisec)
        )

        self.__xnodemap.xNodeMapPoll(elapsed_time_millisec)

    def lock(self):
        """
        **--------------------------------------------------------------**\
        **---------------------------------------------------------------**
        """
        # TODO SFW-2286
        self.__xnodemap.xNodeMapLock()

    def unlock(self):
        """
        **--------------------------------------------------------------**\
        **---------------------------------------------------------------**
        """
        # TODO SFW-2286
        self.__xnodemap.xNodeMapUnlock()

    def try_to_lock(self):
        """
        **--------------------------------------------------------------**\
        **---------------------------------------------------------------**
        """
        # TODO SFW-2286
        return self.__xnodemap.xNodeMapTryLock()

    # feature_names -------------------------------------------------------

    def __get_feature_names(self):
        # have to read it everytime because some features might become
        # unavailable under certain settings
        num_of_nodes = self.__xnodemap.xNodeMapGetNumNodes()
        nodes_names = []
        for node_index in range(num_of_nodes):
            hxnode = self.__xnodemap.xNodeMapGetNodeByIndex(node_index)
            node_ = _node.Node(hxnode)
            if node_.is_feature:
                specific_node = _node_helpers.cast_from_general_node_to_specific_node_type(
                    node_)
                nodes_names.append(specific_node.name)

        return sorted(nodes_names)

    feature_names = property(__get_feature_names)
    """
    A ``list`` of feature nodes' names.
    
    :getter: Returns the current default number of buffers.
    :type: ``list`` of ``str``.\n

    :warning:\n
    - any node becomes unavailable would not show in the \
    feature_names list.\n
    - expensive to call because ``arena_api`` acquires all nodes\
    in the node map then check if ``_node.is_feature`` evaluates to true.
    **------------------------------------------------------------------**\
    **-------------------------------------------------------------------**
    """

    # get_node ------------------------------------------------------------
    def __getitem__(self, key):
        if isinstance(key, str):
            try:
                return self.__get_node(key)
            except ValueError as ve:
                raise KeyError(str(ve))
        else:
            raise TypeError(f'expected str instead of '
                            f'{type(key).__name__}')

    def get_node(self, nodes_names):
        """
        Gets a node or multiple nodes from the node map.\n
        To retrieve a single node there are two ways:
            - ``nodemap.get_node('node_name')`` and
            - ``nodemap['node_name']``

        **Args**:
            nodes_names : it can be:\n
                - a ``str``.\n
                - a ``list`` of ``str``.\n
                - a ``tuple`` of ``str``.\n
        **Raises**:
            - ``ValueError`` :
                - ``nodes_names`` is a ``list`` or ``tuple`` but has an\
                element that is not a ``str``
                - ``nodes_names`` value does not match any node name in\
                this node map
            - ``TypeError`` :
                - ``nodes_names`` type is not ``list``, ``tuple`` nor ``str``.\
                The exception will suggest similar node names.

        **Returns**:
            - a ``dict``, that has node name as a key and the node\
            is the value, if ``nodes_names`` is a ``list``.\n
            - a ``node`` instance when ``nodes_names`` is a str.\n

        **Examples**:\n
            - single node:\n
                >>> height_node = device.nodemap.get_node('Height')
                >>> height_node.value = height_node.max
                >>> print(f'height value is {height_node.value} pxls)
                height value is 2500 pxls

            - multiple nodes:\n
                >>> nodes = device.nodemap.get_node(['Width', Height'])
                >>> # width
                >>> nodes['Width'].value = nodes['Width'].max
                >>> # height
                >>> height_node = nodes['Height']
                >>> height_node.value = height_node.max
                >>> print(f'Image buffer size will be '
                >>>       f'{nodes['Width'].value} by '
                >>>       f'{height_node.value} pxls')
                Image buffer size will be 3000 by 2500 pxls
        **--------------------------------------------------------------**\
        **---------------------------------------------------------------**
        """
        # get a dict from list of node names
        if isinstance(nodes_names, list):
            return self.__get_nodes_as_dict(nodes_names)

        # tuple
        elif isinstance(nodes_names, tuple):
            return self.__get_nodes_as_dict(list(nodes_names))

        elif isinstance(nodes_names, str):
            # get one from node name
            return self.__get_node(nodes_names)
        else:
            raise ValueError(f'expected list, tuple , or str '
                             f'instead of {type(nodes_names).__name__}')

    def __get_nodes_as_dict(self, nodes_names):

        self.__check__get_nodes_as_dict_input_parameter_nodes_names(
            nodes_names)

        specific_nodes = {}
        for node_name in nodes_names:
            specific_nodes[node_name] = self.__get_node(node_name)
        return specific_nodes

    def __check__get_nodes_as_dict_input_parameter_nodes_names(self,
                                                               nodes_names):
        for name in nodes_names:
            if not isinstance(name, str):
                raise ValueError('expected list/tuple str elements instead of '
                                 f'{type(nodes_names).__name__}')

    def __get_node(self, node_name):

        # input is already checked if it is a str or not
        hxnode = self.__xnodemap.xNodeMapGetNode(node_name)

        if not hxnode:
            possible_names = self.__find_closest_matches_to_node_name(
                node_name)
            if not possible_names:
                raise ValueError(f'\'{node_name}\' node does not exist '
                                 f'in this nodemap. Make sure the node name '
                                 f'is correct or check another nodemap\n')
            else:
                raise ValueError(f'\'{node_name}\' node does not exist in '
                                 f'this nodemap\n'
                                 f'(some suggestions):\n'
                                 f'{possible_names}')

        node_ = _node.Node(hxnode)
        specific_node = _node_helpers.cast_from_general_node_to_specific_node_type(
            node_)
        return specific_node

    def __find_closest_matches_to_node_name(self, find_this):
        all_nodes_names = self.feature_names
        close = difflib.get_close_matches(
            find_this, all_nodes_names, n=16, cutoff=0.15)
        return close

    def write_streamable_node_values_to(self, file_name=None):
        """
        Read streamable features from a nodemap and save to a file

        **Args**:\n
            file_name
                - Pass relative path file name as a string
                - If None passed a file will be generated\n
                  <device serialnumber>_<device user id>_<nodemap_type_name>.txt\n
                  ex. 190400015_PHX050S-P_MY_DEVICE_ID_device_nodemap.txt
        **Raises**:\n
            - ``TypeError`` :
                - ``file_name`` is not a string
        **Returns**:\n
            - ``None``.
        """

        nodemap_name = self._nodemap_type_name

        if file_name is None:

            if ('device_nodemap' in nodemap_name or
                    'device_tl_device_nodemap' in nodemap_name):

                device_model_name = self.__xnodemap.xNodeMapGetStringValue(
                    'DeviceModelName')
                device_serial_number = self.__xnodemap.xNodeMapGetStringValue(
                    'DeviceSerialNumber')
                device_user_id = self.__xnodemap.xNodeMapGetStringValue(
                    'DeviceUserID')

                file_name = device_serial_number + \
                    '_' + device_model_name + '_' + device_user_id + \
                    '_' + nodemap_name + '.txt'
            else:
                file_name = nodemap_name + '.txt'

        elif not isinstance(file_name, str):
            raise TypeError(
                f'{str.__name__} '
                f'expected instead of {type(file_name).__name__}')

        xfeature_stream = _xFeaturestream(self.__xnodemap.h_nodemap.value)
        xfeature_stream.xFeatureStreamWriteFileName(file_name)

    def read_streamable_node_values_from(self, file_name):
        """
        Read streamable features from a file and write
        to the corresponding node map

          **Args**:\n
            file_name
                - Pass relative path name of the file stored on
                  machine as a string
        **Raises**:\n
            - ``TypeError`` :
                - ``file_name`` is not a string
        **Returns**:\n
            - ``None``.
        """
        if not isinstance(file_name, str):
            raise TypeError(
                f'{str.__name__} '
                f'expected instead of {type(file_name).__name__}')

        xfeature_stream = _xFeaturestream(self.__xnodemap.h_nodemap.value)
        xfeature_stream.xFeatureStreamReadFileName(file_name)
