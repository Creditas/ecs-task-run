import argparse
import json
import os
import sys

from .client import Client


def run_task(cluster_name, image_name, task_family):
    if cluster_name is None:
        raise Exception('argument --cluster should not be none')
    if task_family is None:
        raise Exception('argument --task should not be none')
    if image_name is None:
        raise Exception('argument --image should not be none')
    client_instance = Client(cluster_name, image_name)
    updated_container = client_instance.update_container(task_family)
    task_id = client_instance.run_task(updated_container, task_family=task_family)
    print('Started task {0}'.format(task_id))
    client_instance.wait_for_task(task_id)
    print('Task output:')

    for log_message in client_instance.get_logs_for_task(updated_container, task_id):
        print('  > {0}'.format(log_message))

    exit_status = client_instance.get_exit_status_for_task(updated_container, task_id)
    print('Task {0} finished with status code:{1}'.format(task_id, exit_status))
    if exit_status != 0:
        sys.exit(exit_status)

def run_update_service(cluster_name, image_name, service_name, task_family):
    if cluster_name is None:
        raise Exception('argument --cluster should not be none')
    if task_family is None:
        raise Exception('argument --task should not be none')
    if image_name is None:
        raise Exception('argument --image should not be none')
    if service_name is None:
        raise Exception('argument --service should not be none')
    try:
        print('Updating Service: {}'.format(service_name))
        client_instance = Client(cluster_name, image_name)
        updated_container = client_instance.update_container(task_family)
        client_instance.update_service(
                container_definition=updated_container,
                service=service_name,
                task_family=task_family,
                )
        print('Updated Service:{}'.format(service_name))
    except Exception as error:
        print('Updated Service Failed:{}'.format(service_name))
        print(error)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='ECS Run')
    parser.add_argument('task_option', help='options:update-service, task, run-config')
    parser.add_argument('--cluster', '-c')
    parser.add_argument('--task', '-t')
    parser.add_argument('--image', '-i')
    parser.add_argument('--service', '-s')
    parser.add_argument('--path', '-p')
    args = parser.parse_args()

    if args.task_option == 'run-config':
        current_full_path = os.path.abspath(os.path.curdir)
        with open(os.path.join(current_full_path, args.path), 'r') as file:
            run_file_list = json.load(file)
        for item_to_run in run_file_list:
            task_option = item_to_run['task_option']
            cluster = item_to_run.get('cluster', None)
            task = item_to_run.get('task', None)
            image = item_to_run.get('image', None)
            service = item_to_run.get('service', None)
            print('Stating to run:{} updated'.format(task_option))
            if task_option == 'task':
                run_task(cluster_name=cluster,
                         task_family=task,
                         image_name=image)
            elif task_option == 'update-service':
                run_update_service(cluster_name=cluster,
                                   task_family=task,
                                   image_name=image,
                                   service_name=service)
        sys.exit(0)

    elif args.task_option == 'task':
        run_task(cluster_name=args.cluster,
                 image_name=args.image,
                 task_family=args.task)
        sys.exit(0)

    elif args.task_option == 'update-service':
        run_update_service(cluster_name=args.cluster,
                           image_name=args.image,
                           task_family=args.task,
                           service_name=args.service)
        sys.exit(0)
    else:
        raise Exception('Invalid task_option, should be: task, update-service, run-config')
