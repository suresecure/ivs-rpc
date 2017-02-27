using System;
using Grpc.Core;
using Suresecureivs;

namespace ivs_event_client
{
    class Program
    {
        public static void Main(string[] args)
        {
            Channel channel = new Channel("127.0.0.1:50051", ChannelCredentials.Insecure);

            var client = new SurvCenterService.SurvCenterServiceClient(channel);
            String user = "you";
            Event nevent = new Event();
            nevent.Description = user;
            AnnotatedImage anno_img = new AnnotatedImage();
            anno_img.Img = Google.Protobuf.ByteString.CopyFrom(new byte[] { 1, 2 });
            Target target = new Target { X = 1, Y = 2, W = 3, H = 4, Type = Target.Types.Type.Person };
            anno_img.Targets.Add(target);
            nevent.AnnoImgs.Add(anno_img);

            var reply = client.ReportEvent(nevent);
            Console.WriteLine("Greeting: " + reply.Message);

            channel.ShutdownAsync().Wait();
            Console.WriteLine("Press any key to exit...");
            Console.ReadKey();
        }
    }
}
