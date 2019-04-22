import boto3
from copy import deepcopy


class Client(object):
    def __init__(self, cluster_name, new_image):
        self.cluster_name = cluster_name
        self.new_image = new_image

        self.ecs_client = boto3.client('ecs')
        self.logs_client = boto3.client('logs')

    def update_container(self, task_family):
        task_definition = self.ecs_client.describe_task_definition(
            taskDefinition=task_family
        )

        new_definition = deepcopy(task_definition)
        new_container = new_definition['taskDefinition']['containerDefinitions'][0]
        new_container['image'] = self.new_image

        return new_container

    def update_service(self, container_definition, task_family, service):
        new_definition_arn = self._update_task_definition(
            container_definition,
            task_family
        )

        self.ecs_client.update_service(
            cluster=self.cluster_name,
            service=service,
            taskDefinition=new_definition_arn
        )

    def run_task(self, container_definition, task_family):
        new_definition_arn = self._update_task_definition(
            container_definition,
            task_family
        )

        task = self.ecs_client.run_task(
            cluster=self.cluster_name,
            taskDefinition=new_definition_arn
        )

        if len(task.get('failures', [])) > 0:
            raise Exception('Run Task Failed - {}'.format(task['failures']))

        return task['tasks'][0]['taskArn'].split('/')[1]

    def wait_for_task(self, task_id):
        self.ecs_client.get_waiter('tasks_stopped').wait(
            cluster=self.cluster_name,
            tasks=[task_id]
        )

    def get_logs_for_task(self, container_definition, task_id):
        container_name = container_definition['name']
        log_options = container_definition['logConfiguration']['options']
        log_prefix = log_options['awslogs-stream-prefix']
        log_cluster_name = log_options['awslogs-group']

        stream_name = "{0}/{1}/{2}".format(log_prefix, container_name, task_id)
        events = self.logs_client.get_log_events(
            logGroupName=log_cluster_name,
            logStreamName=stream_name
        )

        return [e['message'] for e in events['events']]

    def _update_task_definition(self, container_definition, task_family):
        registered = self.ecs_client.register_task_definition(
            family=task_family,
            containerDefinitions=[container_definition]
        )

        return registered['taskDefinition']['taskDefinitionArn']

    def get_exit_status_for_task(self, task_id):
        task_info = self.ecs_client.describe_tasks(
            cluster=self.cluster_name,
            tasks=[task_id]
        )['tasks'][0]
        return task_info['containers'][0]['exitCode']
