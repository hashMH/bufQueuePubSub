import json
import random

class BufferedQueue():
    queue_map = {}
    queue_size = 6

    def __init__(self, queue_map=None, queue_size=None):
        if queue_map:
            self.queue_map = queue_map
        if queue_size:
            self.queue_size = queue_size

    def enqueue(self, key, value):
        print key, value
        if key not in self.queue_map:
            self.queue_map[key] = []
        self.queue_map[key].append(value)
        if len(self.queue_map[key]) >= self.queue_size:
            message = self.queue_map[key]
            self.queue_map[key] = []
            return message
        return None

    def get_buffered_queue_state(self):
        return {'map':self.queue_map, 'buffer_size':self.queue_size}

    def save_state(self):
        json.dump(self.get_buffered_queue_state(), open('buffer_queue.json', 'w'))

    def send_demo_data(self):
        keys = ['apple', 'orange', 'bq3']
        for _ in range(50):
            self.enqueue(random.choice(keys), random.randint(0,100))