#include <iostream>
#include <memory>
#include <string>

#include <grpc++/grpc++.h>

#include "event.grpc.pb.h"

using grpc::Channel;
using grpc::ClientAsyncResponseReader;
using grpc::ClientContext;
using grpc::CompletionQueue;
using grpc::Status;
using suresecureivs::Event;
using suresecureivs::ReportEventReply;
using suresecureivs::EventReporting;

class EventReportingClient {
 public:
  explicit EventReportingClient (std::shared_ptr<Channel> channel)
      : stub_(EventReporting::NewStub(channel)) {}

  // Assembles the client's payload, sends it and presents the response back
  // from the server.
  std::string ReportEvent(const std::string& user) {
    // Data we are sending to the server.
    Event request;
    request.set_description(user);

    // Container for the data we expect from the server.
    ReportEventReply reply;

    // Context for the client. It could be used to convey extra information to
    // the server and/or tweak certain RPC behaviors.
    ClientContext context;

    // The producer-consumer queue we use to communicate asynchronously with the
    // gRPC runtime.
    CompletionQueue cq;

    // Storage for the status of the RPC upon completion.
    Status status;

    // stub_->AsyncSayHello() performs the RPC call, returning an instance we
    // store in "rpc". Because we are using the asynchronous API, we need to
    // hold on to the "rpc" instance in order to get updates on the ongoing RPC.
    std::unique_ptr<ClientAsyncResponseReader<ReportEventReply> > rpc(
        stub_->AsyncReportEvent(&context, request, &cq));

    // Request that, upon completion of the RPC, "reply" be updated with the
    // server's response; "status" with the indication of whether the operation
    // was successful. Tag the request with the integer 1.
    rpc->Finish(&reply, &status, (void*)1);
    void* got_tag;
    bool ok = false;
    // Block until the next result is available in the completion queue "cq".
    cq.Next(&got_tag, &ok);

    // Verify that the result from "cq" corresponds, by its tag, our previous
    // request.
    GPR_ASSERT(got_tag == (void*)1);
    // ... and that the request was completed successfully. Note that "ok"
    // corresponds solely to the request for updates introduced by Finish().
    GPR_ASSERT(ok);

    // Act upon the status of the actual RPC.
    if (status.ok()) {
      return reply.message();
    } else {
      return "RPC failed";
    }
  }

 private:
  // Out of the passed in Channel comes the stub, stored here, our view of the
  // server's exposed services.
  std::unique_ptr<EventReporting::Stub> stub_;
};

int main(int argc, char** argv) {
  // Instantiate the client. It requires a channel, out of which the actual RPCs
  // are created. This channel models a connection to an endpoint (in this case,
  // localhost at port 50051). We indicate that the channel isn't authenticated
  // (use of InsecureChannelCredentials()).
  EventReportingClient greeter(grpc::CreateChannel(
      "localhost:50051", grpc::InsecureChannelCredentials()));
  std::string user("world");
  std::string reply = greeter.ReportEvent(user);  // The actual RPC call!
  std::cout << "Greeter received: " << reply << std::endl;

  return 0;
}
