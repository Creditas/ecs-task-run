import argparse
from .client import Client


def main():

    parser = argparse.ArgumentParser(description='ECS Task Run')
    parser.add_argument('--cluster')
    parser.add_argument('--task')
    parser.add_argument('--image')
    args = parser.parse_args()
    cluster_name = args.cluster
    task_family = args.task
    image_name = args.image

    client = Client(cluster_name, image_name)
    updated_container = client.update_container(task_family)
    task_id = client.run_task(updated_container, task_family=task_family)

    client.wait_for_task(task_id)
    print('Task {0} finished'.format(task_id))
    print('Task output:')

    for log_message in client.get_logs_for_task(updated_container, task_id):
        print('  > {0}'.format(log_message))
