import json

from confluent_kafka.cimpl import KafkaException

from app import bp_main
from flask import request

from app.kafka import KafkaAdminClient
from app.utils import cluster_config

@bp_main.get('/topics/<topic>/groups/<group_id>/consumer_offsets')
def get_topic_consumer_offsets(topic, group_id):
    cluster_id = request.args.get('cluster_id')
    admin_client = KafkaAdminClient({'bootstrap.servers': cluster_config.get_cluster(cluster_id)})
    return json.dumps(admin_client.list_consumer_partition_offsets(topic, group_id))


