
curl -X GET -H "Content-Type: application/json" http://127.0.0.1:8080/restconf/config/Container/

curl -X GET -H "Content-Type: application/json" http://127.0.0.1:8080/restconf/config/Image/


curl -X POST -H "Content-Type: application/json" http://127.0.0.1:8080/restconf/config/Container/c1/ -d'{"ContainerId":"c1", "Image":"ubuntuplus", "Name":"container1", "Ip":"10.50.0.5/24" }'

curl -DELETE -H "Content-Type: application/json" http://127.0.0.1:8080/restconf/config/Container/c1/

