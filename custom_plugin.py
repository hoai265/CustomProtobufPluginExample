import io
import json
import sys

from google.protobuf import json_format
from google.protobuf.compiler import plugin_pb2 as plugin
import custom_options_pb2


def generate_json_file(request, response):
    for proto_file in request.proto_file:
        if proto_file.package == 'my_custom.protobuf':
            file_data = []
            file_json = json_format.MessageToJson(proto_file)
            file_data.append(file_json)

            f_src = response.file.add()
            f_src.name = proto_file.name + '.json'
            f_src.content = json.dumps(file_data, indent=2).encode().decode('unicode_escape')


def message_has_private_field(message):
    for field in message.field:
        if field.options and field.options.HasExtension(custom_options_pb2.custom):
            if field.options.Extensions[custom_options_pb2.custom].private_field:
                return True


def gen_private_tags_header_for_message(message):
    message_data = 'const int ' + message.name + '_private_tags[] = {\n'
    for field in message.field:
        if field.options and field.options.HasExtension(custom_options_pb2.custom):
            if field.options.Extensions[custom_options_pb2.custom].private_field:
                message_data += str(field.number) + ',\n'
    message_data += '};\n\n'
    return message_data


def has_private_field(proto_file):
    for message in proto_file.message_type:
        if message_has_private_field(message):
            return True


def get_file_by_name(name, file_list):
    for file in file_list:
        if file.name == name:
            return file
    return None


def gen_file_header(proto_file):
    header = ''
    header += '#ifndef PB_{}_PRIVATE_TAGS_H_\n'.format(str(proto_file.name).split('.')[0].upper())
    header += '#define PB_{}_PRIVATE_TAGS_H_\n\n'.format(str(proto_file.name).split('.')[0].upper())
    header += '#include "stdint.h"\n'
    header += "\n"
    return header


def generate_private_field_tag_for_file(proto_file):
    file_content = ''
    file_content += gen_file_header(proto_file)

    for message in proto_file.message_type:
        if message_has_private_field(message):
            file_content += gen_private_tags_header_for_message(message)

    file_content += '#endif'
    return file_content


def get_custom_proto_file_list(request):
    proto_files = []
    for proto_file in request.proto_file:
        if proto_file.package == "my_custom.protobuf":
            proto_files.append(proto_file)
    return proto_files


def generate_private_tag_header_file(request, response):
    custom_proto_files = get_custom_proto_file_list(request)
    for proto_file in custom_proto_files:
        if has_private_field(proto_file):
            output_file = response.file.add()
            output_file.name = str(proto_file.name).split('.')[0] + '_private_tags.h'
            output_file.content = generate_private_field_tag_for_file(proto_file)


if __name__ == '__main__':
    # Read request message from stdin
    data = io.open(sys.stdin.fileno(), "rb").read()
    request = plugin.CodeGeneratorRequest.FromString(data)

    # Create response
    response = plugin.CodeGeneratorResponse()

    # Generate code
    generate_json_file(request, response)

    generate_private_tag_header_file(request, response)

    # Serialise response message
    open(sys.stdout.fileno(), "wb").write(response.SerializeToString())
