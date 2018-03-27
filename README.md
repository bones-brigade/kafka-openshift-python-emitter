# kafka-openshift-python-emitter
A Python source-to-image application skeleton for emitting to an Apache Kafka topic

This application will simply take a source URI for a file and then send the
lines from that file to the topic and brokers specified through the environment
variables.

## Launching on OpenShift

```
oc new-app centos/python-27-centos7~https://github.com/bones-brigade/kafka-openshift-python-emitter \
  -e KAFKA_BROKERS=kafka:9092 \
  -e KAFKA_TOPIC=bones-brigade \
  -e SOURCE_URI=https://www.gutenberg.org/files/11/11-0.txt \
  --name=emitter
```

You will need to adjust the `KAFKA_BROKERS` and `KAFKA_TOPICS` variables to
match your configured Kafka deployment and desired topic. The `SOURCE_URI`
environment variable allows you to specify the source file to emit from, in
this example it will use _Alice's Adventures in Wonderland_ from the project
Gutenberg archives.
