
#include <iostream>
#include <memory>
#include <string>

#include "event_async_client2.h"

//#include <grpc++/grpc++.h>
//#include <thread>

//#include "suresecureivs.grpc.pb.h"

// using grpc::Channel;
// using grpc::ClientAsyncResponseReader;
// using grpc::ClientContext;
// using grpc::CompletionQueue;
// using grpc::Status;
// using suresecureivs::Event;
// using suresecureivs::GeneralReply;
// using suresecureivs::EventReporting;
// using suresecureivs::AnnotatedImage;
// using suresecureivs::Target;
// using suresecureivs::Target_Type_person;

EventReportingClient::EventReportingClient(std::shared_ptr<Channel> channel)
    : stub_(EventReporting::NewStub(channel)) {
  // Spawn reader thread that loops indefinitely
  cq_thread_ = std::make_shared<std::thread>(
      &EventReportingClient::AsyncCompleteRpc, this);

  // detach thread is a bad idea
  // we may delete the client object before the thread exit,
  // but the thread func still access the client object
  // std::thread cq_thread(&EventReportingClient::AsyncCompleteRpc, this);
  // cq_thread.detach();
}

// Assembles the client's payload and sends it to the server.
void EventReportingClient::ReportEvent(const Event &e) {
  // Call object to store rpc data
  AsyncClientCall *call = new AsyncClientCall;

  // stub_->AsyncSayHello() performs the RPC call, returning an instance to
  // store in "call". Because we are using the asynchronous API, we need to
  // hold on to the "call" instance in order to get updates on the ongoing
  // RPC.
  call->response_reader = stub_->AsyncReportEvent(&call->context, e, &cq_);

  // Request that, upon completion of the RPC, "reply" be updated with the
  // server's response; "status" with the indication of whether the operation
  // was successful. Tag the request with the memory address of the call
  // object.
  call->response_reader->Finish(&call->reply, &call->status, (void *)call);
}

EventReportingClient::~EventReportingClient() {
  // must shutdown the completion queue and wait join the thread
  Shutdown();
  Wait();
}

void EventReportingClient::Shutdown() { cq_.Shutdown(); }

void EventReportingClient::Wait() {
  if (cq_thread_ != nullptr)
    cq_thread_->join();
}

// Loop while listening for completed responses.
// Prints out the response from the server.
void EventReportingClient::AsyncCompleteRpc() {
  void *got_tag;
  bool ok = false;

  // Block until the next result is available in the completion queue "cq".
  while (cq_.Next(&got_tag, &ok)) {
    // The tag in this example is the memory location of the call object
    AsyncClientCall *call = static_cast<AsyncClientCall *>(got_tag);

    // Verify that the request was completed successfully. Note that "ok"
    // corresponds solely to the request for updates introduced by Finish().
    GPR_ASSERT(ok);

    if (call->status.ok())
      std::cout << "Greeter received: " << call->reply.message() << std::endl;
    else
      std::cout << "RPC failed" << std::endl;

    // Once we're complete, deallocate the call object.
    delete call;
  }
  // we can delete this here, only if the thread is detached
  // or exception occured, because the thread object is a member of this
  // it will be deleted too, which means the thread object is deleted before
  // the thread func over
  // if (cq_thread_ == nullptr)
  // delete this;
}

int main(int argc, char **argv) {

  // Instantiate the client. It requires a channel, out of which the actual RPCs
  // are created. This channel models a connection to an endpoint (in this case,
  // localhost at port 50051). We indicate that the channel isn't authenticated
  // (use of InsecureChannelCredentials()).
  std::shared_ptr<EventReportingClient> client =
      std::make_shared<EventReportingClient>(grpc::CreateChannel(
          "localhost:50051", grpc::InsecureChannelCredentials()));
  // EventReportingClient *client = new
  // EventReportingClient(grpc::CreateChannel(
  //"localhost:50051", grpc::InsecureChannelCredentials()));

  Event event;
  event.set_description("hello");
  AnnotatedImage *anno_img = event.add_anno_imgs();
  anno_img->set_img("kkk");
  Target *target = anno_img->add_targets();
  target->set_type(Target_Type_person);
  target->set_x(1);
  for (int i = 0; i < 100; i++) {
    client->ReportEvent(event); // The actual RPC call!
  }

  return 0;
}
