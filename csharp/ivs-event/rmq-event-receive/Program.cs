using RabbitMQ.Client;
using RabbitMQ.Client.Events;
using System;
using System.Text;
using Suresecureivs;

namespace rmq_event_receive
{
    class Receive
    {
        public static void Main()
        {
            var factory = new ConnectionFactory() { HostName = "localhost" };
            using (var connection = factory.CreateConnection())
            using (var channel = connection.CreateModel())
            {
                channel.QueueDeclare(queue: "event-publish-queue",
                                     durable: false,
                                     exclusive: false,
                                     autoDelete: false,
                                     arguments: null);

                var consumer = new EventingBasicConsumer(channel);
                consumer.Received += (model, ea) =>
                {
                    var body = ea.Body;
                    Event nevent = Event.Parser.ParseFrom(body);
                    //var message = Encoding.UTF8.GetString(body);
                    Console.WriteLine(" [x] Received {0}", nevent.Description);
                };
                channel.BasicConsume(queue: "event-publish-queue",
                                     noAck: true,
                                     consumer: consumer);

                Console.WriteLine(" Press [enter] to exit.");
                Console.ReadLine();
            }
        }
    }
}
