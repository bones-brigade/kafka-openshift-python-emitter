import argparse
import importlib.machinery as importlib
import logging
import os
import time
import types
import urllib.request as urllib

from kafka import KafkaProducer


def external_file_generator(args):
    logging.info('downloading source')
    dl = urllib.urlretrieve(args.source)
    sourcefile = open(dl[0])
    logging.info('sending lines')
    for line in sourcefile.readlines():
        yield line
    logging.info('finished sending source')


def main(args):
    logging.info('brokers={}'.format(args.brokers))
    logging.info('topic={}'.format(args.topic))
    logging.info('rate={}'.format(args.rate))
    logging.info('source={}'.format(args.source))

    # if a user function is specified, download it and import it
    if args.userfunction is not None:
        try:
            logging.info('downloading user function')
            logging.info(args.userfunction)
            dl = urllib.urlretrieve(args.userfunction)[0]
            loader = importlib.SourceFileLoader('userfunction', dl)
            userfunction = types.ModuleType(loader.name)
            loader.exec_module(userfunction)
            emitter_function = userfunction.user_defined_function
            logging.info('user function loaded')
        except Exception as e:
            logging.error('failed to import user function file')
            logging.error(e)
            emitter_function = None
    else:
        logging.info(
                'no user function specified, using external file generator')
        emitter_function = external_file_generator

    logging.info('creating kafka producer')
    producer = KafkaProducer(bootstrap_servers=args.brokers)

    logging.info('beginning producer loop')
    if emitter_function is not None:
        for i in emitter_function(args):
            producer.send(args.topic, i.encode())
            time.sleep(1.0 / args.rate)
    logging.info('ending producer loop')


def get_arg(env, default):
    return os.getenv(env) if os.getenv(env, '') is not '' else default


def parse_args(parser):
    args = parser.parse_args()
    args.brokers = get_arg('KAFKA_BROKERS', args.brokers)
    args.topic = get_arg('KAFKA_TOPIC', args.topic)
    args.rate = get_arg('RATE', args.rate)
    args.source = get_arg('SOURCE_URI', args.source)
    args.userfunction = get_arg('USER_FUNCTION_URI', args.userfunction)
    return args


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    logging.info('starting kafka-python emitter')
    parser = argparse.ArgumentParser(description='emit some stuff on kafka')
    parser.add_argument(
            '--brokers',
            help='The bootstrap servers, env variable KAFKA_BROKERS',
            default='localhost:9092')
    parser.add_argument(
            '--topic',
            help='Topic to publish to, env variable KAFKA_TOPIC',
            default='bones-brigade')
    parser.add_argument(
            '--rate',
            type=int,
            help='Lines per second, env variable RATE',
            default=3)
    parser.add_argument(
            '--source',
            help='The source URI for data to emit, env variable SOURCE_URI')
    parser.add_argument(
            '--user-function',
            dest='userfunction',
            help='URI to a user function .py file, env variable '
            'USER_FUNCTION_URI')
    args = parse_args(parser)
    main(args)
    logging.info('exiting')
