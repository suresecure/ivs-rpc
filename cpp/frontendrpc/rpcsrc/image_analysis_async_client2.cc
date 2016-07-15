
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
using suresecureivs::ImageRegion;
using suresecureivs::ImageClassifyReply;
using suresecureivs::ImageAnalysis;

// Assembles the client's payload and sends it to the server.
void ImageAnalysisClient::ImageClassify(const ImageRegion &image_region) {
  // Data we are sending to the server.
  // Event request;
  // request.set_description(user);

  // Call object to store rpc data
  AsyncClientCall *call = new AsyncClientCall;

  // stub_->AsyncSayHello() performs the RPC call, returning an instance to
  // store in "call". Because we are using the asynchronous API, we need to
  // hold on to the "call" instance in order to get updates on the ongoing RPC.
  call->response_reader =
      stub_->AsyncImageClassify(&call->context, image_region, &cq_);

  // Request that, upon completion of the RPC, "reply" be updated with the
  // server's response; "status" with the indication of whether the operation
  // was successful. Tag the request with the memory address of the call object.
  call->response_reader->Finish(&call->reply, &call->status, (void *)call);
}

// Loop while listening for completed responses.
// Prints out the response from the server.
void ImageAnalysisClient::AsyncCompleteRpc() {
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
      std::cout << "Greeter received: " << call->reply.type() << std::endl;
    else
      std::cout << "RPC failed" << std::endl;

    // Once we're complete, deallocate the call object.
    delete call;
  }
}
