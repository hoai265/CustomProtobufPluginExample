rm -rf dist
mkdir dist

protoc --proto_path=. --python_out=. custom_options.proto
pyinstaller --onefile custom_plugin.py