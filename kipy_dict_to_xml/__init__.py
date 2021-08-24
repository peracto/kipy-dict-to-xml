from .data_xml_pipe import data_xml_pipe
from .buffered_bytearray_pipe import buffered_bytearray_pipe
from .string_concat_pipe import string_concat_pipe, string_concat_byte_pipe
from .iterator_reader import IteratorReader


def create_reader(data_generator, **kwargs):
    return IteratorReader(string_concat_byte_pipe(data_xml_pipe(data_generator=data_generator, **kwargs)))

