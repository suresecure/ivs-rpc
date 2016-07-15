
#include <iostream>
#include <memory>
#include <string>

#include <grpc++/grpc++.h>
#include <thread>

#include "suresecureivs.grpc.pb.h"

using grpc::Channel;
using grpc::ClientAsyncResponseReader;
using grpc::ClientContext;
using grpc::CompletionQueue;
using grpc::Status;
using suresecureivs::Event;
using suresecureivs::GeneralReply;
using suresecureivs::EventReporting;
using suresecureivs::AnnotatedImage;
using suresecureivs::Target;
using suresecureivs::Target_Type_person;

class EventReportingClient {
public:
  explicit EventReportingClient(std::shared_ptr<Channel> channel);
  ~EventReportingClient();
  void ReportEvent(const Event &e);

  void Shutdown();
  void Wait();
  void AsyncCompleteRpc();

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

