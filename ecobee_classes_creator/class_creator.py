import builtins
import inspect
import keyword
import logging
import textwrap

import black

from ecobee_classes_creator.scraper import Scraper
from ecobee_classes_creator.utilities import Utility

logger = logging.getLogger(__name__)


class ClassCreator(object):
    @classmethod
    def run(cls):
        types_map = {
            'Boolean': 'bool',
            'Enum': 'six.text_type',
            'Integer': 'int',
            'Map': 'Dict[six.text_type, object]',
            'String': 'six.text_type',
        }
        vowels = {'A', 'E', 'I', 'O', 'U'}

        module_body = None
        imports = None
        class_body = None
        class_name = None
        module_code = {}
        slots = None
        attribute_name_map = None
        attribute_type_map = None
        constructor_signature = None
        constructor_docstring = None
        constructor_body = None
        properties = None

        for (line_index, line) in enumerate(Scraper.get_scraped_lines()):
            logger.debug('Processing line #%s -> %s', line_index + 1, line.strip())

            line_tokens = line.split()

            if len(line_tokens) == 2:
                if line_index != 0:
                    slots.append(
                        ', '.join(
                            module_code['required_attribute']['slots']
                            + module_code['not_required_attribute']['slots']
                        )
                    )
                    slots.append(']\n\n')

                    attribute_name_map.append(
                        ', '.join(
                            module_code['required_attribute']['attribute_name_map']
                            + module_code['not_required_attribute'][
                                'attribute_name_map'
                            ]
                        )
                    )
                    attribute_name_map.append('}\n\n')

                    attribute_type_map.append(
                        ', '.join(
                            module_code['required_attribute']['attribute_type_map']
                            + module_code['not_required_attribute'][
                                'attribute_type_map'
                            ]
                        )
                    )
                    attribute_type_map.append('}\n\n')

                    constructor_signature.append(
                        ', '.join(
                            module_code['required_attribute']['constructor_signature']
                            + module_code['not_required_attribute'][
                                'constructor_signature'
                            ]
                        )
                    )
                    constructor_signature.append('):\n')

                    constructor_body.append(
                        '\n'.join(
                            module_code['required_attribute']['constructor_body']
                            + module_code['not_required_attribute']['constructor_body']
                        )
                    )
                    constructor_body.append('\n\n')

                    properties.append(
                        '\n'.join(
                            module_code['required_attribute']['properties']
                            + module_code['not_required_attribute']['properties']
                        )
                    )
                    properties.append('\n\n')

                    class_body.append(''.join(slots))
                    class_body.append(''.join(attribute_name_map))
                    class_body.append(''.join(attribute_type_map))
                    class_body.append(''.join(constructor_signature))
                    class_body.append(constructor_docstring)
                    class_body.append(''.join(constructor_body))
                    class_body.append(''.join(properties))
                    module_body.append(''.join(imports))
                    module_body.append(''.join(class_body))

                    with open(
                        'objects/{0}.py'.format(
                            Utility.camel_case_to_underscore_case(class_name).lower()[
                                1:
                            ]
                        ),
                        'w',
                        encoding='utf-8',
                    ) as output_file:
                        output_file.write(
                            black.format_str(
                                '{0}\n'.format(''.join(module_body).strip()),
                                mode=black.FileMode(string_normalization=False),
                            )
                        )

                module_body = []
                imports = ['from pyecobee.ecobee_object import EcobeeObject\n\n']
                class_body = []
                class_name = line_tokens[0].strip()
                class_url = line_tokens[1].strip()
                module_body.append(
                    '"""\nThis module is home to the {0} class\n"""\n'.format(
                        class_name
                    )
                )
                class_body.append('class {0}(EcobeeObject):\n'.format(class_name))
                class_body.append('    """\n')
                class_body.append(
                    '    This class has been auto generated by scraping\n    '
                )
                class_body.append('{0}\n'.format(class_url))
                class_body.append('\n')
                class_body.append(
                    '{0}\n'.format(
                        '\n'.join(
                            textwrap.wrap(
                                '    Attribute names have been generated by converting '
                                'ecobee property names from camelCase to snake_case.',
                                72,
                                subsequent_indent=' ' * 4,
                            )
                        )
                    )
                )
                class_body.append('\n')
                class_body.append(
                    '    A getter property has been generated for each attribute.\n'
                )
                class_body.append(
                    '{0}\n'.format(
                        '\n'.join(
                            textwrap.wrap(
                                '    A setter property has been generated for each '
                                'attribute whose value of READONLY is "no".',
                                72,
                                subsequent_indent=' ' * 4,
                            )
                        )
                    )
                )
                class_body.append('\n')
                class_body.append(
                    '{0}\n'.format(
                        '\n'.join(
                            textwrap.wrap(
                                '    An __init__ argument without a default value has '
                                'been generated if the value of REQUIRED is "yes".',
                                72,
                                subsequent_indent=' ' * 4,
                            )
                        )
                    )
                )
                class_body.append(
                    '{0}\n'.format(
                        '\n'.join(
                            textwrap.wrap(
                                '    An __init__ argument with a default value of None '
                                'has been generated if the value of REQUIRED is "no".',
                                72,
                                subsequent_indent=' ' * 4,
                            )
                        )
                    )
                )
                class_body.append('    """\n')
                module_code = {
                    'required_attribute': {
                        'attribute_name_map': [],
                        'attribute_type_map': [],
                        'constructor_body': [],
                        'constructor_signature': [],
                        'properties': [],
                        'slots': [],
                    },
                    'not_required_attribute': {
                        'attribute_name_map': [],
                        'attribute_type_map': [],
                        'constructor_body': [],
                        'constructor_signature': [],
                        'properties': [],
                        'slots': [],
                    },
                }
                slots = ['    __slots__ = [']
                attribute_name_map = ['    attribute_name_map = {']
                attribute_type_map = ['    attribute_type_map = {']
                constructor_signature = ['    def __init__(self, ']
                constructor_docstring = (
                    '        """\n'
                    '        Construct a{0} {1} instance\n'
                    '        """\n'.format(
                        'n' if class_name[0] in vowels else '', class_name
                    )
                )
                constructor_body = []
                properties = []
            else:
                attribute_name = Utility.camel_case_to_underscore_case(line_tokens[0])

                parameter_name = attribute_name
                if (
                    parameter_name in list(zip(*inspect.getmembers(builtins)))[0]
                    or parameter_name in keyword.kwlist
                ):
                    parameter_name = '{0}_'.format(parameter_name)

                index = line_tokens[1].find('[')

                if index != -1:
                    attribute_type = (
                        types_map[line_tokens[1][0:index]]
                        if line_tokens[1][0:index] in types_map
                        else line_tokens[1][0:index]
                    )
                    attribute_type = 'List[{0}]'.format(attribute_type)
                else:
                    attribute_type = (
                        types_map[line_tokens[1]]
                        if line_tokens[1] in types_map
                        else line_tokens[1]
                    )

                is_attribute_readonly = line_tokens[2] == 'yes'
                is_attribute_required = line_tokens[3] == 'yes'

                if is_attribute_required:
                    module_code_key = 'required_attribute'
                else:
                    module_code_key = 'not_required_attribute'

                module_code[module_code_key]['slots'].append(
                    "'_{0}'".format(attribute_name)
                )
                module_code[module_code_key]['attribute_name_map'].append(
                    "'{0}': '{1}'".format(attribute_name, line_tokens[0])
                )
                if attribute_name != line_tokens[0]:
                    module_code[module_code_key]['attribute_name_map'].append(
                        "'{0}': '{1}'".format(line_tokens[0], attribute_name)
                    )

                module_code[module_code_key]['attribute_type_map'].append(
                    "'{0}': '{1}'".format(attribute_name, attribute_type)
                )

                if is_attribute_required:
                    module_code[module_code_key]['constructor_signature'].append(
                        '{0}'.format(parameter_name)
                    )
                else:
                    module_code[module_code_key]['constructor_signature'].append(
                        '{0}=None'.format(parameter_name)
                    )

                module_code[module_code_key]['constructor_body'].append(
                    '        self._{0} = {1}'.format(attribute_name, parameter_name)
                )

                getter = '{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}'.format(
                    '    @property\n',
                    '    def {0}(self):\n'.format(attribute_name),
                    '        """\n',
                    '{0}\n'.format(
                        '\n'.join(
                            textwrap.wrap(
                                '        Gets the {0} attribute of this {1} '
                                'instance.'.format(attribute_name, class_name),
                                72,
                                subsequent_indent=' ' * 8,
                            )
                        )
                    ),
                    '\n',
                    '{0}\n'.format(
                        '\n'.join(
                            textwrap.wrap(
                                '        :return: The value of the {0} attribute of '
                                'this {1} instance.'.format(attribute_name, class_name),
                                72,
                                subsequent_indent=' ' * 8,
                            )
                        )
                    ),
                    '        :rtype: {0}\n'.format(attribute_type),
                    '        """\n',
                    '\n',
                    '        return self._{0}\n'.format(attribute_name),
                )
                module_code[module_code_key]['properties'].append(getter)

                if not is_attribute_readonly:
                    setter = '{0}{1}{2}{3}{4}{5}{6}{7}{8}{9}'.format(
                        '    @{0}.setter\n'.format(attribute_name),
                        '    def {0}(self, {1}):\n'.format(
                            attribute_name, parameter_name
                        ),
                        '        """\n',
                        '{0}\n'.format(
                            '\n'.join(
                                textwrap.wrap(
                                    '        Sets the {0} attribute of this {1} '
                                    'instance.'.format(attribute_name, class_name),
                                    72,
                                    subsequent_indent=' ' * 8,
                                )
                            )
                        ),
                        '\n',
                        '{0}\n'.format(
                            '\n'.join(
                                textwrap.wrap(
                                    '        :param {0}: The {0} value to set for the '
                                    '{0} attribute of this {1} instance.'.format(
                                        attribute_name, class_name
                                    ),
                                    72,
                                    subsequent_indent=' ' * 8,
                                )
                            )
                        ),
                        '        :type: {0}\n'.format(attribute_type),
                        '        """\n',
                        '\n',
                        '        self._{0} = {1}\n'.format(
                            attribute_name, parameter_name
                        ),
                    )

                    module_code[module_code_key]['properties'].append(setter)
