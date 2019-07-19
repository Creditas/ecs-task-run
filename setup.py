import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ecs_task_run",
    version="0.0.7",
    author="Aurelio Saraiva",
    author_email="aurelio.saraiva@creditas.com.br",
    description="ECS Task Definition run",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/creditas/ecs-task-run",
    packages=setuptools.find_packages(),
    entry_points={"console_scripts": ["ecs-task-run=ecs_task_run:main",
                                      "ecs-run=ecs_task_run:ecs_run"]},
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        "boto3"
    ]
)
