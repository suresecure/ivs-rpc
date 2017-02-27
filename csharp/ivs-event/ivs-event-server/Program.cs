using System;
using System.Threading.Tasks;
using Grpc.Core;
using Suresecureivs;

namespace ivs_event_server
{
    //实现接收报警服务
    class EventReporttingImpl : EventReporting.EventReportingBase
    {
        // Server side handler of the SayHello RPC
        public override Task<ReportEventReply> ReportEvent(Event request, ServerCallContext context)
        {
            //接收到报警以后简单回复
            Console.WriteLine(request.AnnoImgs);
            return Task.FromResult(new ReportEventReply { Message = "Hello " + request.Description });
        }
    }

    class Program
    {
        const int Port = 50051;

        public static void Main(string[] args)
        {
            //新建服务器，并绑定服务
            Server server = new Server
            {
                Services = { EventReporting.BindService(new EventReporttingImpl()) },
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
