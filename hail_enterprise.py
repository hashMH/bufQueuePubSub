import json
import os
import sys
import random
from buffered_queue import BufferedQueue
from abstract_message_queue import AbstractMessageQueue

if os.path.isfile('buffer_queue.json'):
	buffered_queue_map = json.load(open("buffer_queue.json"))
	buffer_queue = BufferedQueue(
						buffered_queue_map['map'],
						buffered_queue_map['buffer_size']
						)
else:
	buffer_queue = BufferedQueue()

message_queue = AbstractMessageQueue('localhost', 'direct')

if len(sys.argv) > 1:
	demo = True if sys.argv[1] == 'demo' else False
	if demo:
		keys = ['bq1', 'bq2', 'bq3']
		for _ in range(50):
			queue_name = random.choice(keys)
			demo_buffer_resp = buffer_queue.enqueue(queue_name, random.randint(0,100))
			if demo_buffer_resp:
				message_queue.publish(queue_name, demo_buffer_resp)

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
