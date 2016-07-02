REM protoc.exe --cpp_out=..\proto-cpp event.suresecureivs.proto analytics.suresecureivs.proto devicemgt.suresecureivs.proto
protoc.exe -I ..\protos --cpp_out=. --grpc_out=. --plugin=protoc-gen-grpc=grpc_cpp_plugin.exe ..\protos\event.proto
