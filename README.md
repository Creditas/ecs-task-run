# ecs-task-run

## Install

```bash
$ pip install ecs-task-run
```

## Create new revision

To create a new release, you need to edit the [setup.py](https://github.com/Creditas/ecs-task-run/blob/master/setup.py#L8) file, stating the number of the new version.

After you merge, the travis-ci pipeline will automatically publish the new version at https://pypi.org/project/ecs-task-run/


## Using

### Running tasks:
```bash
$ ecs-task-run --cluster YOUR_CLUSTER_NAME --task YOUR_TASK_DEFINITION --image YOUR_IMAGE
```
or:
```bash
$ ecs-run task --cluster YOUR_CLUSTER_NAME --task YOUR_TASK_DEFINITION --image YOUR_IMAGE
```
or:
```bash
$ ecs-run task -c YOUR_CLUSTER_NAME -t YOUR_TASK_DEFINITION -i YOUR_IMAGE
```

### Updating Services:
```bash
$ ecs-run update-service --cluster YOUR_CLUSTER_NAME --task YOUR_TASK_DEFINITION --image YOUR_IMAGE --service YOUR_SERVICE_NAME
```
or:
```bash
$ ecs-run update-service -c YOUR_CLUSTER_NAME -t YOUR_TASK_DEFINITION -i YOUR_IMAGE -s YOUR_SERVICE_NAME
```

### Running a deploy config
To run a list of jobs from a file.
```bash
ecs-run run-jobs --path LOCAL_PATH_TO_CONFIG
```
or
```bash
ecs-run run-jobs -p LOCAL_PATH_TO_CONFIG
```

Example config:
```json
[{
"job_option":"task",
"task":"YOUR_TASK_DEFINITION",
"image":"YOUR_IMAGE",
"cluster":"YOUR_CLUSTER_NAME"
},
{
"job_option":"update-service",
"task":"YOUR_TASK_DEFINITION",
"service":"YOUR_SERVICE_NAME",
"image":"YOUR_IMAGE",
"cluster":"YOUR_CLUSTER_NAME"
}]
```


