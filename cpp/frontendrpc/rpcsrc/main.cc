#include <iostream>
#include <fstream>
#include <sstream>
#include <memory>
#include <string>
#include <thread>
#include <unistd.h>
#define _WIN32_WINNT 0x0600
#include <grpc++/grpc++.h>

#include "device_rpc.h"
#include "suresecureivs.grpc.pb.h"

int main(int argc, char **argv) {
  // RpcServer rpc_server;
  // rpc_server.StartInThread();
  // sleep(10);
  // rpc_server.ShutdownInThread();
  // return 0;

  std::shared_ptr<Channel> channel = grpc::CreateChannel("localhost:50051", grpc::InsecureChannelCredentials());
  // EventReportingClient greeter(grpc::CreateChannel(
  //"localhost:50051", grpc::InsecureChannelCredentials()));

  // for (int i = 0; i < 100; i++) {
  // Event e;
  // e.set_description("hello");
  // greeter.ReportEvent(e); // The actual RPC call!
  //}

  // std::cout << "Press control-c to quit" << std::endl
  //<< std::endl;
  // sleep(2);
  // greeter.Wait();

  ImageAnalysisClient greeter(channel);

  for (int i = 0; i < 100; i++) {
    ImageRegion image_region;
    std::ifstream fin("/home/mythxcq/2.jpg", std::ios::binary);
    std::string img;
    std::ostringstream ostrm;
    ostrm << fin.rdbuf();
    image_region.set_img(ostrm.str());
    image_region.set_x(0);
    image_region.set_y(1);
    image_region.set_w(2);
    image_region.set_h(3);
    greeter.ImageClassify(image_region); // The actual RPC call!
  }

  std::cout << "Press control-c to quit" << std::endl
            << std::endl;
  //sleep(2);
  greeter.ShutdownAndWait();
}
