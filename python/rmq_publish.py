#!/usr/bin/env python
import pika
import event_pb2

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='event-publish-queue')

nevent = event_pb2.Event()
nevent.type = event_pb2.Event.evt_people_appr
nevent.description = "no"

body = nevent.SerializeToString()
print body

channel.basic_publish(exchange='',
                      routing_key='event-publish-queue',
                      body=body)
print(" [x] Sent 'Hello World!'")
connection.close()

# if __name__ == '__main__':
  # serve()
