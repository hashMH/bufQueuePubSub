import json
import os
from bufferedQueue import BufferedQueue
from abstractMessageQueue import AbstractMessageQueue

if os.path.isfile('buffer_queue.json'):
	buffered_queue_map = json.load(open("buffer_queue.json"))
	buffer_queue = BufferedQueue(
						buffered_queue_map['map'],
						buffered_queue_map['buffer_size']
						)
else:
	buffer_queue = BufferedQueue()

message_queue = AbstractMessageQueue('localhost', 'direct')

while True:
	queue_name = raw_input("Enter Queue Name or Enter q or quit: ")

	if str.lower(queue_name) == 'q' or str.lower(queue_name) == 'quit':
		buffer_queue.save_state()
		break

	message = raw_input("Enter Element for your Buffer Message: ")

	buffer_resp = buffer_queue.enqueue(queue_name, message)
	if buffer_resp:
		state = message_queue.publish(queue_name, buffer_resp)
		if not state:
			buffer_queue.save_state()
			break
