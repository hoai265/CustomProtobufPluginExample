# CustomProtobufPluginExample
An example about making a custom Protocol Buffers plugin in python with custom options

# What is Protocol Buffers :

https://developers.google.com/protocol-buffers

https://github.com/protocolbuffers/protobuf

# Plugin

We defined an custom option for protocol buffer in custom_options.proto.
And we use this custom option in our test.proto as an example.

Plugin read the input .proto files and generate an header .h file based on that.
Header .h file contain information about which fields use custom options in our custom_options.proto.

# Generate plugin

Run 'gen_plugin.sh' to generate our custom plugin

# Use plugin

After plugin has generated.
Run 'run_plugin.sh' to use plugin.
