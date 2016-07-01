
#include <iostream>
#include <memory>
#include <string>

#include <grpc++/grpc++.h>

#include "event.grpc.pb.h"

using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;
using suresecureivs::Event;
using suresecureivs::ReportEventReply;
using suresecureivs::EventReporting;

class EventReportingClient {
 public:
  EventReportingClient(std::shared_ptr<Channel> channel)
      : stub_(EventReporting::NewStub(channel)) {}

  // Assambles the client's payload, sends it and presents the response back
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

    // The actual RPC.
    Status status = stub_->ReportEvent(&context, request, &reply);

    // Act upon its status.
    if (status.ok()) {
      return reply.message();
    } else {
      return "RPC failed";
    }
  }

 private:
  std::unique_ptr<EventReporting::Stub> stub_;
};

int main(int argc, char** argv) {
  // Instantiate the client. It requires a channel, out of which the actual RPCs
  // are created. This channel models a connection to an endpoint (in this case,
  // localhost at port 50051). We indicate that the channel isn't authenticated
  // (use of InsecureChannelCredentials()).
  EventReportingClient reporter(grpc::CreateChannel(
      "localhost:50051", grpc::InsecureChannelCredentials()));
  std::string user("world");
  std::string reply = reporter.ReportEvent(user);
  std::cout << "Reporter received: " << reply << std::endl;

  return 0;
}
