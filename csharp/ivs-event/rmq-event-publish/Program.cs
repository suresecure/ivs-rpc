using System;
using RabbitMQ.Client;
using System.Text;
using Suresecureivs;
using Google.Protobuf;
using System.IO;

namespace rmq_event_publish
{
class Send
{
    public static void Main()
    {
        var factory = new ConnectionFactory() { HostName = "localhost" };
        using(var connection = factory.CreateConnection())
        using(var channel = connection.CreateModel())
        {
            channel.QueueDeclare(queue: "event-publish-queue",
                                 durable: false,
                                 exclusive: false,
                                 autoDelete: false,
                                 arguments: null);

            Event nevent = new Event();
            nevent.Description = "yes";
            nevent.Type = Event.Types.Type.EvtNone;
            //Event.Parser.ParseFrom()
            byte[] body;
            using (var ms = new MemoryStream())
            {
                nevent.WriteTo(ms);
                body = ms.ToArray();
            }

            channel.BasicPublish(exchange: "",
                                 routingKey: "event-publish-queue",
                                 basicProperties: null,
                                 body: body);
            Console.WriteLine(" [x] Sent {0}", "x");
        }

        Console.WriteLine(" Press [enter] to exit.");
        Console.ReadLine();
    }
}
}