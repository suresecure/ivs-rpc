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
    class SurvCenterServiceImpl : SurvCenterService.SurvCenterServiceBase
    {
        // Server side handler of the SayHello RPC
        public override Task<GeneralReply> ReportEvent(Event request, ServerCallContext context)
        {
            Console.WriteLine(request.AnnoImgs);
            return Task.FromResult(new GeneralReply { Message = "Hello " + request.Description });
        }
    }

    class Program
    {
        const int Port = 50051;

        public static void Main(string[] args)
        {
            Server server = new Server
            {
                Services = { SurvCenterService.BindService(new SurvCenterServiceImpl()) },
                Ports = { new ServerPort("localhost", Port, ServerCredentials.Insecure) }
            };
            server.Start();

            Console.WriteLine("Greeter server listening on port " + Port);
            Console.WriteLine("Press any key to stop the server...");
            Console.ReadKey();

            server.ShutdownAsync().Wait();
        }
    }
}
