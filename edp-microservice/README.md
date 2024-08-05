PoC for Event Details Page microservice

EDP microservice provide information about markets and outcomes related to interesetd event through SocketIO conector.
In case when new market or outcome apears or desapears microservice send new part of actual data to client through SocketIO conector.

### Building ###
gradle clean build

### Execution ###
java -jar edp-microservice-0.0.1.jar

### Specific options ###

Port for providing demo page
--server.port=9090

Port for SocketIO connector
--socketio.port=8080
