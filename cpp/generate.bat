protoc.exe --cpp_out=..\proto-cpp event.suresecureivs.proto analytics.suresecureivs.proto devicemgt.suresecureivs.proto
protoc.exe --grpc_out=..\proto-cpp --plugin=protoc-gen-grpc=grpc_cpp_plugin.exe event.suresecureivs.proto analytics.suresecureivs.proto devicemgt.suresecureivs.proto
