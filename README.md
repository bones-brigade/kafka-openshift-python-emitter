# kafka-openshift-python-emitter
A Python source-to-image application skeleton for emitting to an Apache Kafka topic

This application will simply take a source URI for a file and then send the
lines from that file to the topic and brokers specified through the environment
variables.

## Launching on OpenShift

```
oc new-app centos/python-27-centos7~https://github.com/bones-brigade/kafka-openshift-python-emitter \
  -e KAFKA_BROKERS=kafka:9092 \
  -e SOURCE_URL=https://www.gutenberg.org/files/11/11-0.txt
```

This will launch the emitter using the default topic of `bones-brigade` and
emitting 3 lines per second from _Alice's Adventures in Wonderland_ source
text on project Gutenberg.
