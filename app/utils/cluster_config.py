__config = {
    'dev': 'localhost：8092'
}

def list_clusters():
    return __config

def get_cluster(cluster_id) -> str:
    return __config[cluster_id]
