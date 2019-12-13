rm -rf dist
mkdir dist
pyinstaller --onefile custom_plugin.py

rm -rf build
mkdir build

protoc --proto_path=. --python_out=. custom_options.proto

protoc --plugin=protoc-gen-custom=dist/custom_plugin --custom_out=./build test.proto