@rem Generate the C# code for .proto files

setlocal

@rem enter this directory
cd /d %~dp0

set TOOLS_PATH=packages\Grpc.Tools.0.15.0\tools\windows_x86

%TOOLS_PATH%\protoc.exe -I../../protos --csharp_out suresecureivs  ../../protos/suresecureivs.proto --grpc_out suresecureivs --plugin=protoc-gen-grpc=%TOOLS_PATH%\grpc_csharp_plugin.exe

endlocal
