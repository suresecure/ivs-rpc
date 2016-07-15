#pragma once
#include <iostream>
#include <memory>
#include <string>
#include <thread>
#include <unistd.h>
#define _WIN32_WINNT 0x0600
#include <grpc++/grpc++.h>

#include "suresecureivs.grpc.pb.h"

using grpc::Server;
using grpc::ServerBuilder;
using grpc::ServerContext;
using grpc::Channel;
using grpc::ClientAsyncResponseReader;
using grpc::ClientContext;
using grpc::CompletionQueue;
using grpc::Status;
using suresecureivs::Empty;
using suresecureivs::Event;
using suresecureivs::NetworkEndpoint;
using suresecureivs::GeneralReply;
using suresecureivs::DeviceMgt;
using suresecureivs::EventReporting;
using suresecureivs::ImageRegion;
using suresecureivs::ImageClassifyReply;
using suresecureivs::ImageAnalysis;
using suresecureivs::EventReporting;
using suresecureivs::ImageRegion;
using suresecureivs::ImageClassifyReply;
using suresecureivs::ImageAnalysis;

class RpcServer;
class DeviceMgtServiceImpl final : public DeviceMgt::Service {
  Status GetHealthyStatus(ServerContext *context, const Empty *request,
                          Empty *response) override;
  Status GetEventServerAddress(ServerContext *context, const Empty *request,
                               NetworkEndpoint *response) override;
  Status SetEventServerAddress(ServerContext *context,
                               const NetworkEndpoint *request,
                               GeneralReply *response) override;
  Status GetImageAnalysisServerAddress(ServerContext *context,
                                       const Empty *request,
                                       NetworkEndpoint *response) override;
  Status SetImageAnalysisServerAddress(ServerContext *context,
                                       const NetworkEndpoint *request,
                                       GeneralReply *response) override;

public:
  DeviceMgtServiceImpl(RpcServer *rpc_server) : rpc_server_(rpc_server) {}

private:
  RpcServer *rpc_server_;
};
class RpcServer {
public:
  RpcServer();
  void Wait() { server_->Wait(); }
  void Shutdown() { server_->Shutdown(); }

  void StartInThread() {
    rpc_thread_ = std::make_shared<std::thread>(&RpcServer::Wait, this);
  }
  void ShutdownInThread() {
    server_->Shutdown();
    rpc_thread_->join();
  }

  const std::string &GetEventServerAddress() { return event_server_address_; }
  int GetEventServerPort() { return event_server_port_; }
  void SetEventServerAddress(const std::string &address) {
    event_server_address_ = address;
  }
  void SetEventServerPort(int port) { event_server_port_ = port; }
  const std::string &GetImageAnalysisServerAddress() {
    return event_server_address_;
  }
  void SetImageAnalysisServerAddress(const std::string &address) {
    image_analysis_server_address_ = address;
  }
  int GetImageAnalysisServerPort() { return image_analysis_server_port_; }
  void SetImageAnalysisServerPort(int port) {
    image_analysis_server_port_ = port;
  }

private:
  std::unique_ptr<Server> server_;
  std::shared_ptr<DeviceMgtServiceImpl> device_mgt_service_impl_;

  std::string event_server_address_;
  int event_server_port_;
  std::string image_analysis_server_address_;
  int image_analysis_server_port_;

  std::shared_ptr<std::thread> rpc_thread_;
};

class EventReportingClient {
public:
  explicit EventReportingClient(std::shared_ptr<Channel> channel)
      : stub_(EventReporting::NewStub(channel)) {
    cq_thread_ = std::make_shared<std::thread>(
        &EventReportingClient::AsyncCompleteRpc, this);
  }

  // Assembles the client's payload and sends it to the server.
  void ReportEvent(const Event &e);
  // Loop while listening for completed responses.
  // Prints out the response from the server.
  void AsyncCompleteRpc();
  void Wait() {
    cq_.Shutdown();
    cq_thread_->join();
  }

private:
  // struct for keeping state and data information
  struct AsyncClientCall {
    // Container for the data we expect from the server.
    GeneralReply reply;

    // Context for the client. It could be used to convey extra information to
    // the server and/or tweak certain RPC behaviors.
    ClientContext context;

    // Storage for the status of the RPC upon completion.
    Status status;

    std::unique_ptr<ClientAsyncResponseReader<GeneralReply>> response_reader;
  };

  // Out of the passed in Channel comes the stub, stored here, our view of the
  // server's exposed services.
  std::unique_ptr<EventReporting::Stub> stub_;

  // The producer-consumer queue we use to communicate asynchronously with the
  // gRPC runtime.
  CompletionQueue cq_;
  std::shared_ptr<std::thread> cq_thread_;
};

class ImageAnalysisClient {
public:
  explicit ImageAnalysisClient(std::shared_ptr<Channel> channel)
      : stub_(ImageAnalysis::NewStub(channel)) {

    cq_thread_ = std::make_shared<std::thread>(&ImageAnalysisClient::AsyncCompleteRpc, this);
  }

  // Assembles the client's payload and sends it to the server.
  void ImageClassify(const ImageRegion &image_region);
  // Loop while listening for completed responses.
  // Prints out the response from the server.
  void AsyncCompleteRpc();
  void ShutdownAndWait()
  {
    cq_.Shutdown();
    cq_thread_->join();
  }

private:
  // struct for keeping state and data information
  struct AsyncClientCall {
    // Container for the data we expect from the server.
    ImageClassifyReply reply;

    // Context for the client. It could be used to convey extra information to
    // the server and/or tweak certain RPC behaviors.
    ClientContext context;

    // Storage for the status of the RPC upon completion.
    Status status;

    std::unique_ptr<ClientAsyncResponseReader<ImageClassifyReply>>
        response_reader;
  };

  // Out of the passed in Channel comes the stub, stored here, our view of the
  // server's exposed services.
  std::unique_ptr<ImageAnalysis::Stub> stub_;

  // The producer-consumer queue we use to communicate asynchronously with the
  // gRPC runtime.
  CompletionQueue cq_;
  std::shared_ptr<std::thread> cq_thread_;
};
