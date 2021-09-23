# coding: utf-8

"""
    AutoMATES Common Abstract Syntax Tree (CAST) v1

    This document outlines the structure of the CAST that will be used as a generic representation of the semantics of a program written in any language. This will be used when creating functions networks from programs using the University of Arizonas program analysis pipeline.    __Generating Class Structure__    To automatically generate Python or Java models corresponding to this document, you can use [swagger-codegen](https://swagger.io/tools/swagger-codegen/). We can use this to generate client code based off of this spec that will also generate the class structure.    1. Install via the method described for your operating system [here](https://github.com/swagger-api/swagger-codegen#Prerequisites). Make sure to install a version after 3.0 that will support openapi 3.  2. Run swagger-codegen with the options in the example below. The URL references where the yaml for this documentation is stored on github. Make sure to replace CURRENT_VERSION with the correct version. To generate Java classes rather, change the `-l python` to `-l java`. Change the value to the `-o` option to the desired output location.       ```      swagger-codegen generate -l python -o ./client -i https://raw.githubusercontent.com/ml4ai/automates-v2/master/docs/source/cast_openapi_v{CURRENT_VERSION}.yaml      ```  3. Once it executes, the client code will be generated at your specified location. For python, the classes will be located in `$OUTPUT_PATH/swagger_client/models/`. For java, they will be located in `$OUTPUT_PATH/src/main/java/io/swagger/client/model/`      # noqa: E501

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""

import pprint
import re  # noqa: F401

import six


class SourceRef(object):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    """
    Attributes:
      swagger_types (dict): The key is attribute name
                            and the value is attribute type.
      attribute_map (dict): The key is attribute name
                            and the value is json key in definition.
    """
    swagger_types = {
        "source_file_name": "str",
        "col_start": "float",
        "col_end": "float",
        "row_start": "float",
        "row_end": "float",
    }
    attribute_map = {
        "source_file_name": "source_file_name",
        "col_start": "col_start",
        "col_end": "col_end",
        "row_start": "row_start",
        "row_end": "row_end",
    }

    def __init__(
        self,
        source_file_name=None,
        col_start=None,
        col_end=None,
        row_start=None,
        row_end=None,
    ):  # noqa: E501
        """SourceRef - a model defined in Swagger"""  # noqa: E501
        self._source_file_name = None
        self._col_start = None
        self._col_end = None
        self._row_start = None
        self._row_end = None
        self.discriminator = None
        if source_file_name is not None:
            self.source_file_name = source_file_name
        if col_start is not None:
            self.col_start = col_start
        if col_end is not None:
            self.col_end = col_end
        if row_start is not None:
            self.row_start = row_start
        if row_end is not None:
            self.row_end = row_end

    @property
    def source_file_name(self):
        """Gets the source_file_name of this SourceRef.  # noqa: E501


        :return: The source_file_name of this SourceRef.  # noqa: E501
        :rtype: str
        """
        return self._source_file_name

    @source_file_name.setter
    def source_file_name(self, source_file_name):
        """Sets the source_file_name of this SourceRef.


        :param source_file_name: The source_file_name of this SourceRef.  # noqa: E501
        :type: str
        """

        self._source_file_name = source_file_name

    @property
    def col_start(self):
        """Gets the col_start of this SourceRef.  # noqa: E501


        :return: The col_start of this SourceRef.  # noqa: E501
        :rtype: float
        """
        return self._col_start

    @col_start.setter
    def col_start(self, col_start):
        """Sets the col_start of this SourceRef.


        :param col_start: The col_start of this SourceRef.  # noqa: E501
        :type: float
        """

        self._col_start = col_start

    @property
    def col_end(self):
        """Gets the col_end of this SourceRef.  # noqa: E501


        :return: The col_end of this SourceRef.  # noqa: E501
        :rtype: float
        """
        return self._col_end

    @col_end.setter
    def col_end(self, col_end):
        """Sets the col_end of this SourceRef.


        :param col_end: The col_end of this SourceRef.  # noqa: E501
        :type: float
        """

        self._col_end = col_end

    @property
    def row_start(self):
        """Gets the row_start of this SourceRef.  # noqa: E501


        :return: The row_start of this SourceRef.  # noqa: E501
        :rtype: float
        """
        return self._row_start

    @row_start.setter
    def row_start(self, row_start):
        """Sets the row_start of this SourceRef.


        :param row_start: The row_start of this SourceRef.  # noqa: E501
        :type: float
        """

        self._row_start = row_start

    @property
    def row_end(self):
        """Gets the row_end of this SourceRef.  # noqa: E501


        :return: The row_end of this SourceRef.  # noqa: E501
        :rtype: float
        """
        return self._row_end

    @row_end.setter
    def row_end(self, row_end):
        """Sets the row_end of this SourceRef.


        :param row_end: The row_end of this SourceRef.  # noqa: E501
        :type: float
        """

        self._row_end = row_end

    def to_dict(self):
        """Returns the model properties as a dict"""
        result = {}

        for attr, _ in six.iteritems(self.swagger_types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(
                    map(lambda x: x.to_dict() if hasattr(x, "to_dict") else x, value)
                )
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(
                    map(
                        lambda item: (item[0], item[1].to_dict())
                        if hasattr(item[1], "to_dict")
                        else item,
                        value.items(),
                    )
                )
            else:
                result[attr] = value
        if issubclass(SourceRef, dict):
            for key, value in self.items():
                result[key] = value

        return result

    def to_str(self):
        """Returns the string representation of the model"""
        return pprint.pformat(self.to_dict())

    def __repr__(self):
        """For `print` and `pprint`"""
        return self.to_str()

    def __eq__(self, other):
        """Returns true if both objects are equal"""
        if not isinstance(other, SourceRef):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """Returns true if both objects are not equal"""
        return not self == other
