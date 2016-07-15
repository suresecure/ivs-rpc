#include <iostream>
#include <memory>
#include <string>

#include <grpc++/grpc++.h>
#include <thread>

#include "device_rpc.h"
#include "suresecureivs.grpc.pb.h"

using grpc::Channel;
using grpc::ClientAsyncResponseReader;
using grpc::ClientContext;
using grpc::CompletionQueue;
using grpc::Status;
using suresecureivs::Event;
using suresecureivs::GeneralReply;
using suresecureivs::EventReporting;

void EventReportingClient::ReportEvent(const Event &e) {
  AsyncClientCall *call = new AsyncClientCall;
  call->response_reader = stub_->AsyncReportEvent(&call->context, e, &cq_);
  call->response_reader->Finish(&call->reply, &call->status, (void *)call);
}

// Loop while listening for completed responses.
// Prints out the response from the server.
void EventReportingClient::AsyncCompleteRpc() {
  void *got_tag;
  bool ok = false;

  while (cq_.Next(&got_tag, &ok)) {
    AsyncClientCall *call = static_cast<AsyncClientCall *>(got_tag);
    GPR_ASSERT(ok);

    if (call->status.ok())
      std::cout << "Greeter received: " << call->reply.message() << std::endl;
    else
      std::cout << "RPC failed" << std::endl;

    delete call;
  }
}
