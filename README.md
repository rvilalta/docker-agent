# docker-agent
This repository contains a docker agent to provide an extended Docker REST (including interconnection to OVS)

You should configure docker REST to port 4243, by adding it as OPT in /etc/default/docker:
DOCKER_OPTS="-H tcp://127.0.0.1:4243 -H unix:///var/run/docker.sock"

Then you can restart docker as:
sudo service docker restart

