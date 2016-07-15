@rem Generate the C# code for .proto files

setlocal

@rem enter this directory
cd /d %~dp0

set PROTOC_PATH=..\thirdparty\protobuf-3.0.0-beta-2\bin
set GRPC_PATH=..\thirdparty\grpc-0-13-1\bin

%PROTOC_PATH%\protoc.exe -I../../protos --cpp_out rpcsrc  ../../protos/event.proto --grpc_out rpcsrc --plugin=protoc-gen-grpc=%GRPC_PATH%\grpc_cpp_plugin.exe

endlocal
