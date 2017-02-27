//using System;
//using System.Collections.Generic;
//using System.Linq;
//using System.Text;
//using System.Threading.Tasks;

//namespace ivs_event_server
//{
//    class Program
//    {
//        static void Main(string[] args)
//        {
//        }
//    }
//}

using System;
using System.Threading.Tasks;
using Grpc.Core;
using Suresecureivs;

namespace ivs_event_server
{
    //服务端实现服务
    class SurvCenterServiceImpl : SurvCenterService.SurvCenterServiceBase
    {
        //实现接收报警事件服务
        public override Task<GeneralReply> ReportEvent(Event request, ServerCallContext context)
        {
            Console.WriteLine(request.AnnoImgs);
            return Task.FromResult(new GeneralReply { Message = "Hello " + request.Description });
        }
        //实现接收心跳服务
        public override Task<GeneralReply> Heartbeat(HeartbeatRequest request, ServerCallContext context)
        {
            Console.WriteLine("Heart Get: " + request.DeviceAddress + ", " + request.DeviceIdent);
            return Task.FromResult(new GeneralReply { Message = "Get heartbeat!" });
        }
    }

    class Program
    {
        const int Port = 50051;

        public static void Main(string[] args)
        {
            //建立服务器，并绑定服务
            Server server = new Server
            {
                Services = { SurvCenterService.BindService(new SurvCenterServiceImpl()) },
                Ports = { new ServerPort("localhost", Port, ServerCredentials.Insecure) }
            };
            //启动服务器
            server.Start();

            Console.WriteLine("Greeter server listening on port " + Port);
            Console.WriteLine("Press any key to stop the server...");
            Console.ReadKey();

            //结束服务器
            server.ShutdownAsync().Wait();
        }
    }
}
