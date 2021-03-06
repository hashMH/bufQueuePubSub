from abstract_message_queue import AbstractMessageQueue
import sys

# This listens to queue for messages by values in argument

message_queue = AbstractMessageQueue('localhost', 'direct')

listening = sys.argv[1:]
if not listening:
	sys.stderr.write("Enterprise is completely offline")
	sys.exit(1)

for each in listening:
	message_queue.bind_listener(each)

print(' -> Waiting for Messages from %s. To exit press CTRL+C' % ', '.join(listening))

message_queue.consumer().start_consuming()