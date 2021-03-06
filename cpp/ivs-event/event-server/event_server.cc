#include <iostream>
#include <memory>
#include <string>
#include <thread>
#include <grpc++/grpc++.h>

#include "suresecureivs.grpc.pb.h"

using grpc::Server;
using grpc::ServerBuilder;
using grpc::ServerContext;
using grpc::Status;
using suresecureivs::Empty;
//using suresecureivs::EventServerAddress;
using suresecureivs::Event;
using suresecureivs::GeneralReply;
using suresecureivs::EventReporting;
//using suresecureivs::DeviceMgt;

// Logic and data behind the server's behavior.
class EventReportingServiceImpl final : public EventReporting::Service {
  Status ReportEvent(ServerContext *context, const Event *request,
                     GeneralReply *reply) override {

    std::cout << request->anno_imgs_size() << std::endl;
    std::cout << request->description() << "\t" << request->hostaddress() << "\t"
              << request->channel() << "\t" << request->person_num() << "\t"
              << request->meter_area_num() << "\t" << request->frontend_version()
              << std::endl;
    // std::string prefix("Hello ");
    // std::cout << std::this_thread::get_id() << std::endl;
    // sleep(4);
    // std::cout << request->anno_imgs_size() << std::endl;
    // if (request->anno_imgs_size() > 0)
    //{
    // std::cout << request->anno_imgs(0).img() << std::endl;
    // std::cout << request->anno_imgs(0).targets_size() << std::endl;
    // if (request->anno_imgs(0).targets_size() > 0)
    //{
    // std::cout << request->anno_imgs(0).targets(0).x() << std::endl;
    //}
    //}
    // std::cout << "request name: " << request->description() << std::endl;
    reply->set_message("ok");
    return Status::OK;
  }
};

// class DeviceMgtServiceImpl final : public DeviceMgt::Service {
// Status GetHealthyStatus(ServerContext *context, const Empty *request,
// Empty *response) override {
// return Status::OK;
//}
// Status GetEventServerAddress(ServerContext *context, const Empty *request,
// EventServerAddress *response) override {
// response->set_address("123");
// return Status::OK;
//}
// Status SetEventServerAddress(ServerContext *context,
// const EventServerAddress *request,
// GeneralReply *response) override {
// response->set_message("yes");
// return Status::OK;
//}
//};

void RunServer() {
  std::string server_address("0.0.0.0:50051");
  EventReportingServiceImpl event_reporting_service;
  //DeviceMgtServiceImpl device_mgt_service;

  ServerBuilder builder;
  // Listen on the given address without any authentication mechanism.
  builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());
  // Register "service" as the instance through which we'll communicate with
  // clients. In this case it corresponds to an *synchronous* service.
  builder.RegisterService(&event_reporting_service);
  // builder.RegisterService(&device_mgt_service);
  // Finally assemble the server.
  std::unique_ptr<Server> server(builder.BuildAndStart());
  std::cout << "Server listening on " << server_address << std::endl;

  // Wait for the server to shutdown. Note that some other thread must be
  // responsible for shutting down the server for this call to ever return.
  server->Wait();
}

int main(int argc, char **argv) {
  RunServer();

  return 0;
}
