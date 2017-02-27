using System;
using Grpc.Core;
using Suresecureivs;

namespace ivs_event_client
{
    class Program
    {
        public static void Main(string[] args)
        {
            //建立通道
            Channel channel = new Channel("127.0.0.1:50051", ChannelCredentials.Insecure);

            //新建客户端
            var client = new SurvCenterService.SurvCenterServiceClient(channel);
            //任意设置一些属性值
            String user = "you";
            //新建报警事件
            Event nevent = new Event();
            nevent.Description = user;
            //新建报警事件图片
            AnnotatedImage anno_img = new AnnotatedImage();
            //将二进制JPEG码流拷贝到报警事件图片中
            anno_img.Img = Google.Protobuf.ByteString.CopyFrom(new byte[] { 1, 2 });
            //设置报警事件图片中的目标
            Target target = new Target { X = 1, Y = 2, W = 3, H = 4, Type = Target.Types.Type.Person };
            anno_img.Targets.Add(target);
            nevent.AnnoImgs.Add(anno_img);

            //向服务器提交报警事件
            var reply = client.ReportEvent(nevent);
            Console.WriteLine("Greeting: " + reply.Message);

            HeartbeatRequest hr = new HeartbeatRequest();
            hr.DeviceAddress = "127.0.0.1";
            hr.DeviceIdent = "i am a deivce";
            //异步调用心跳请求
            var hr_reply = client.HeartbeatAsync(hr);
            //等待异步操作返回，具体实现时可以使用完整异步机制
            hr_reply.ResponseAsync.Wait();
            Console.WriteLine("Heartbeat over: "+ hr_reply.ResponseAsync.Result);

            channel.ShutdownAsync().Wait();
            Console.WriteLine("Press any key to exit...");
            Console.ReadKey();
        }
    }
}
