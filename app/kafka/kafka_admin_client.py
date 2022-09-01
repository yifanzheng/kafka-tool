
from confluent_kafka.admin import AdminClient
from confluent_kafka.cimpl import Consumer, TopicPartition, KafkaException, OFFSET_INVALID



class KafkaAdminClient(object):
    def __init__(self, config):
        self.config = config
        self.client = AdminClient(config)

    def list_topics(self, timeout=-1):
        cluster_metadata = self.client.list_topics(timeout=timeout)  # ClusterMetadata
        topic_metadatas = cluster_metadata.topics  # TopicMetadata
        return [topic_name for topic_name in topic_metadatas]

    def get_topic(self, topic_name):
        topic_info = {}
        cluster_metadata = self.client.list_topics(topic_name)  # ClusterMetadata
        topic_meta = cluster_metadata.topics
        if topic_meta[topic_name].error is not None:
            raise KafkaException(topic_meta[topic_name][topic_name].error)

        topic_info['topic_name'] = topic_name
        topic_info['partitions'] = len(topic_meta[topic_name].partitions.keys())
        return topic_info

    def list_groups(self):
        groups = self.client.list_groups()
        print(groups)

    def list_consumer_partition_offsets(self, topic_name, group_id):
        consumer_config = self.config
        consumer_config['client.id'] = 'query-consumer-offsets'
        consumer_config['group.id'] = group_id
        consumer_config['enable.auto.commit'] = 'false'

        return self.__list_partition_offsets(consumer_config, topic_name)

    def __list_partition_offsets(self, conf, topic_name):
        result = []
        consumer = Consumer(conf)
        try:
            topic_metadata = consumer.list_topics(topic_name, timeout=10)
            if topic_metadata.topics[topic_name].error is not None:
                raise KafkaException(topic_metadata.topics[topic_name].error)

            # Construct TopicPartition list of partitions to query
            partitions = [TopicPartition(topic_name, partition) for partition in
                          list(topic_metadata.topics[topic_name].partitions.keys())]

            # Query committed offsets for this group and the given partitions
            committed = consumer.committed(partitions, timeout=10)
            for p in committed:
                (low_offset, high_offset) = consumer.get_watermark_offsets(p, timeout=10)
                if p.offset == OFFSET_INVALID:
                    offset = '-'
                else:
                    offset = p.offset
                if high_offset < 0:
                    lag = 'no hwmark'  # Unlikely
                elif p.offset < 0:
                    # No committed offset, show total message count as lag.
                    # The actual message count may be lower due to compaction
                    # and record deletions.
                    lag = high_offset - low_offset
                else:
                    lag = high_offset - p.offset
                result.append({'partition': p.partition,
                               'start_offset': low_offset,
                               'end_offset': high_offset,
                               'offset': offset,
                               'lag': lag
                               })
        finally:
            consumer.close()

        return result
