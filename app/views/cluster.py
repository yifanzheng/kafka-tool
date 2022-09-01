import json

from app import bp_main
from app.utils import cluster_config
from app.kafka.kafka_admin_client import KafkaAdminClient


@bp_main.get("/clusters")
def list_clusters():
    return json.dumps(cluster_config.list_clusters())


@bp_main.get('/clusters/<string:cluster_id>/topics')
def list_topics(cluster_id):
    admin_client = KafkaAdminClient({'bootstrap.servers': cluster_config.get_cluster(cluster_id)})
    admin_client.list_groups()
    return json.dumps(admin_client.list_topics())


@bp_main.get("/clusters/<string:cluster_id>/topics/<topic>")
def get_topic(cluster_id, topic):
    admin_client = KafkaAdminClient({'bootstrap.servers': cluster_config.get_cluster(cluster_id)})
    return json.dumps(admin_client.get_topic(topic))
