# bufQueuePubSub

bufQueuePubSub is a Publisher and Subscriber with a buffered Queue pattern to control messages.

### Description
Definition of a "buffered queue"
*  Hash map of queues
*  Each value in the hashmap acts like a queue
*  Each value (queue) has a fixed buffer size
*  Each queue is auto popped when buffer size is reached and queued data is sent to the listening subscribers

### Usage pattern
* Publisher sends data into a buffered queue BQi with key Qi & buffer size Bi
* Subscribers subscribe to various buffer queues BQi (0 < i < n)

Example: Consider a buffered queue BQ with data [2,3,4,5,6] & buffer size B=6. Assume subscribers S1 and S2 are subscribing to it. On enqueuing the 6th element, let's say its 7, BQ becomes empty [] and the queue [2,3,4,5,6,7] is sent to the listening subscribers S1 and S2.

AbstractMessageQueue.py -- Its a wrapper for rabbitMq pika.
BufferedQueue.py -- Its has buffered queue mechanism to control publishing
hail_enterprise.py -- Its a publisher that takes user input and sends it across to enterprise(subscriber)

>python hail_enterprise.py                                   
>Enter Queue Name or Enter q or quit: apple                                                                              
>Enter Element for your Buffer Message: 1  

enterprise_respond.py -- It''s enterprises receiver module, which can selectively listen to keys

>python enterprise_respond.py apple orange      
>-> Waiting for Messages from apple, orange. To exit press CTRL+C 

Two instances of *enterprise_respond.py* listening to same key will receive messages simultaneously.
