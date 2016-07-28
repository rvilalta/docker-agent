
curl -X GET -H "Content-Type: application/json" http://127.0.0.1:8080/restconf/config/Container/

curl -X GET -H "Content-Type: application/json" http://127.0.0.1:8080/restconf/config/Image/


curl -X POST -H "Content-Type: application/json" http://127.0.0.1:8080/restconf/config/Container/container1/ -d'{"ContainerId":"container1", "Image":"ubuntuplus", "Ip":"10.50.0.5/24" }'

curl -X DELETE -H "Content-Type: application/json" http://127.0.0.1:8080/restconf/config/Container/container1/

curl -X POST -H "Content-Type: application/json" http://127.0.0.1:8080/restconf/operations/ContainerExec/ -d'{"ContainerId":"container1", "Command":"echo \"Hello\""}'
