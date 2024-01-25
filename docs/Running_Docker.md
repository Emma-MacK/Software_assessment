### Running Docker ###

This document described how to build and run the docker.
This was built and tested in a branch from develop at commit 544b5f5

The docker allows a container to be build. This container has all the requirement to run the tool.

First the Docker image needs to be build from the Docker file

```
docker build . -t test_docker
```

The first time this is run a permission error may occur. This can be resolved using `sudo chmod 666 /var/run/docker.sock`, which gives docker permission to interact with files

Once the docker image has been created, a container can be started with the following command:

```
docker run -dit --name test_docker test_docker:latest
```
This creates an active container that can be used to run commands.

```
docker run test_docker python Draft_scripts/tool_v2.py -ID R24
```

#### Example ####

The following examples were run in a conda environment that did not have the tool requirements present.

**Before Docker**

```
python Draft_scripts/tool_v2.py

Traceback (most recent call last):
  File "/home/emma/Documents/Uni_work/software/Software_assessment/Draft_scripts/tool_v2.py", line 7, in <module>
    import pandas as pd
  File "/home/emma/.local/lib/python3.10/site-packages/pandas/__init__.py", line 16, in <module>
    raise ImportError(
ImportError: Unable to import required dependencies:
pytz: No module named 'pytz'
dateutil: No module named 'dateutil'

```

**Using Docker**

```
docker run test_docker python Draft_scripts/tool_v2.py -ID R24

R code found in test directory:
FGFR3 c.1138
{'detail': 'Not found.'}
```


When docker is used, the required dependencies are found where they previously not available.

**Using Docker to run the frontend**

First build the docker

```
docker build -t test_docker .
```


Then run the following command :

```
docker run -p 8000:8000 -v $(pwd):/code test_docker python frontend/manage.py runserver 0.0.0.0:8000
```

Finally access the frontend through the url:

http://127.0.0.1:8000/
