# kafka-python-emitter
A Python application skeleton for emitting to an Apache Kafka topic

This application will simply take a source URI for a file and then send the
lines from that file to the topic and brokers specified through the environment
variables.

## Deploying on OpenShift

These instructions show how to deploy the emitter on [OpenShift](https://okd.io)
using the [command line client tool](https://docs.okd.io/latest/cli_reference/get_started_cli.html).

### Prerequisites

* A terminal shell with the OpenShift client tool (`oc`) available.

* An active login to an OpenShift project

### Procedure

* Launch the emitter using the following command
  ```
  oc new-app centos/python-36-centos7~https://gitlab.com/bones-brigade/kafka-python-emitter.git \
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

## Customizing the emitter function

You can change the behavior of the emitter by supplying a generator function
that will get polled at the rate specified. The user defined function that you
supply must be a generator that accepts a single argument and returns a string.
The arguments provided will be a wrapper to the application configuration. For
an example see the [emitter.py](examples/emitter.py) file.

To utilize an external user defined function it must exist in a file that
can be downloaded by your continerized application. The environment
variable `USER_FUNCTION_URI` must contain the URI to the file. Here is an
example using the previous launch command and the `emitter.py` file from this
repository:

```
oc new-app centos/python-36-centos7~https://gitlab.com/bones-brigade/kafka-python-emitter.git \
-e KAFKA_BROKERS=kafka:9092 \
-e KAFKA_TOPIC=bones-brigade \
-e USER_FUNCTION_URI=https://gitlab.com/bones-brigade/kafka-python-emitter/raw/master/examples/emitter.py
--name=emitter
```

### User defined function API

The API for creating a user defined function is fairly simple, there are three
rules to crafting a function:

1. There must be a top-level function named `user_defined_function`. This
   is the main entry point into your feature, the main application will look
   for this function.
1. Your function must accept a single argument. The function will be passed
   a namespace object containing the application configuration options.
1. Your function must return either a string. That string will get emitted
   onto the kafka topic for the application.
