#include <iostream>
#include <memory>
#include <string>
#include <thread>
#define _WIN32_WINNT 0x0600
#include <grpc++/grpc++.h>

#include "device_rpc.h"

#include "suresecureivs.grpc.pb.h"

using grpc::Server;
using grpc::ServerBuilder;
using grpc::ServerContext;
using grpc::Status;
using suresecureivs::Empty;
using suresecureivs::NetworkEndpoint;
using suresecureivs::GeneralReply;
using suresecureivs::DeviceMgt;

Status DeviceMgtServiceImpl::GetHealthyStatus(ServerContext *context,
                                              const Empty *request,
                                              Empty *response) {
  return Status::OK;
}
Status DeviceMgtServiceImpl::GetEventServerAddress(
    ServerContext *context, const Empty *request,
    NetworkEndpoint *response) {
  response->set_address("123");
  return Status::OK;
}
Status
DeviceMgtServiceImpl::SetEventServerAddress(ServerContext *context,
                                            const NetworkEndpoint *request,
                                            GeneralReply *response) {
  response->set_message("yes");
  return Status::OK;
}
Status DeviceMgtServiceImpl::GetImageAnalysisServerAddress(
    ServerContext *context, const Empty *request,
    NetworkEndpoint *response) {
  return Status::OK;
}
Status DeviceMgtServiceImpl::SetImageAnalysisServerAddress(
    ServerContext *context, const NetworkEndpoint *request,
    GeneralReply *response) {
  return Status::OK;
}

RpcServer::RpcServer() {
  std::string server_address("0.0.0.0:50051");
  // EventReportingServiceImpl event_reporting_service;
  ServerBuilder builder;
  // Listen on the given address without any authentication mechanism.
  builder.AddListeningPort(server_address, grpc::InsecureServerCredentials());
  // Register "service" as the instance through which we'll communicate with
  // clients. In this case it corresponds to an *synchronous* service.
  // builder.RegisterService(&device_mgt_service);
  device_mgt_service_impl_ = std::make_shared<DeviceMgtServiceImpl>(this);
  builder.RegisterService(device_mgt_service_impl_.get());
  // Finally assemble the server.
  server_ = builder.BuildAndStart();
}
