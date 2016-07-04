#!/usr/bin/env python
import pika
import event_pb2

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost'))
channel = connection.channel()

channel.queue_declare(queue='event-publish-queue')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    nevent = event_pb2.Event()
    nevent.ParseFromString(body)
    print nevent.description
    print nevent.type

channel.basic_consume(callback,
                      queue='event-publish-queue',
                      no_ack=True)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
