# ecs-task-run

## Install

```bash
$ pip install ecs-task-run
```

## Using

### Running tasks:
```bash
$ ecs-task-run task --cluster YOUR_CLUSTER_NAME --task YOUR_TASK_DEFINITION --image YOUR_IMAGE
```
or:
```bash
$ ecs-task-run task -c YOUR_CLUSTER_NAME -t YOUR_TASK_DEFINITION -i YOUR_IMAGE
```

### Updating Services:
```bash
$ ecs-task-run update-service --cluster YOUR_CLUSTER_NAME --task YOUR_TASK_DEFINITION --image YOUR_IMAGE --service YOUR_SERVICE_NAME
```
or:
```bash
$ ecs-task-run update-service -c YOUR_CLUSTER_NAME -t YOUR_TASK_DEFINITION -i YOUR_IMAGE -s YOUR_SERVICE_NAME
```

### Running a deploy config
To run a list of jobs from a file.
```bash
ecs-task-run run-config --path LOCAL_PATH_TO_CONFIG
```
or
```bash
ecs-task-run run-config -p LOCAL_PATH_TO_CONFIG
```

Example config:
```json
[{
"task_option":"task",
"task":"YOUR_TASK_DEFINITION",
"image":"YOUR_IMAGE",
"cluster":"YOUR_CLUSTER_NAME"
},
{
"task_option":"update-service",
"task":"YOUR_TASK_DEFINITION",
"service":"YOUR_SERVICE_NAME",
"image":"YOUR_IMAGE",
"cluster":"YOUR_CLUSTER_NAME"
}]
```


