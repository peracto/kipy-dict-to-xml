import inspect
from .utility import escape, quote_attr


_pretty_levels = ['\n' + "\t" * (i + 1) for i in range(40)]
_not_pretty_levels = ['' for i in range(40)]


def data_xml_pipe(data_generator, root_tag=None, item_tag=None, pretty_print=False):

    if not inspect.isgenerator(data_generator):
        raise ValueError("Expected Generator")

    yield f'<?xml version="1.0" encoding="utf-8"?>\n<{root_tag}>'

    pretty_levels = _pretty_levels if pretty_print else _not_pretty_levels

    for j in data_generator:
        current_iter = iter({item_tag: j}.items())
        is_dict = True
        list_key = None
        stack = []
        level = 0
        pretty_level = pretty_levels[0]

        while True:
            try:
                while True:
                    key, value = next(current_iter) if is_dict is True else (list_key, next(current_iter))

                    if key == '#text':
                        yield escape(str(value))
                        continue

                    if isinstance(value, dict):
                        if key.startswith('#'):  # Signals start of an object encoded with attributes
                            stack.append((key[1:], is_dict, list_key, current_iter))
                            yield f"{pretty_level}<{key[1:]}"
                            for ik, iv in value.items():
                                if ik.startswith('@'):
                                    yield f' {ik[1:]}="{quote_attr(iv)}"'
                            current_iter = (v for v in value.items() if not v[0].startswith('@'))
                            yield ">"
                        else:
                            stack.append((key, is_dict, list_key, current_iter))
                            current_iter = iter(value.items())
                            yield f"{pretty_level}<{key}>"

                        level = level + 1
                        is_dict = True
                        list_key = None
                        pretty_level = pretty_levels[level]
                    elif isinstance(value, str):
                        yield f"{pretty_level}<{key}>{escape(value)}</{key}>"
                    elif value is None:
                        yield f"{pretty_level}<{key}/>"
                    elif isinstance(value, bool):
                        yield f"{pretty_level}<{key}>{'true' if value is True else 'false'}</{key}>"
                    elif isinstance(value, (int, float)):
                        yield f"{pretty_level}<{key}>{value}</{key}>"
                    elif not hasattr(value, '__iter__'):
                        yield f"{pretty_level}<{key}>{escape(str(value))}</{key}>"
                    else:  # iterable
                        stack.append((key, is_dict, list_key, current_iter))
                        is_dict = False
                        list_key = key
                        current_iter = iter(value)
            except StopIteration:
                if len(stack) == 0:
                    break
                was_dict = is_dict
                key, is_dict, list_key, current_iter = stack.pop()

                level = level - 1
                pretty_level = pretty_levels[level]

                if was_dict is True:
                    yield f"{pretty_level}</{key}>"

    yield f"\n</{root_tag}>"
