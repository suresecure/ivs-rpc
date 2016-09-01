using System;
using Grpc.Core;
using Suresecureivs;

namespace ivs_event_client
{
    class Program
    {
        public static void Main(string[] args)
        {
            //Channel channel = new Channel("127.0.0.1:50051", ChannelCredentials.Insecure);
            Channel channel = new Channel("192.168.3.42:50051", ChannelCredentials.Insecure);

            var client = new ImageAnalysis.ImageAnalysisClient(channel);
            ImageRegion image_region = new ImageRegion();
            byte[] byteArray = System.IO.File.ReadAllBytes("1.jpg");
            image_region.Img = Google.Protobuf.ByteString.CopyFrom(byteArray);
            //anno_img.Img = Google.Protobuf.ByteString.CopyFrom(new byte[] { 1, 2 });
            AsyncUnaryCall<ObjectDetectionReply> reply_call = client.ObjectDetectionAsync(image_region);
            ObjectDetectionReply reply = reply_call.ResponseAsync.Result;

            Console.WriteLine("return code: " + reply.GeneralReply.ErrorCode);
            if (reply.GeneralReply.ErrorCode == 0)
            {
                foreach (ObjectTarget t in reply.Targets)
                {
                    Console.WriteLine("Person: " + t.X + " " + t.Y + " " + t.W + " " + t.H + " " + t.Type);
                }
            }

            channel.ShutdownAsync().Wait();
            Console.WriteLine("Press any key to exit...");
            Console.ReadKey();
        }
    }
}
