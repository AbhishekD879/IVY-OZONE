Quck Bet microservice allows to place single bets without UI Betslip.
Communitation with Front-End through SocketIO

### Building ###
gradle clean build

### Execution ###
java -jar build/libs/quickbet-microservice-100-SNAPSHOT.jar

### Specific options ###

Port for providing demo page
--server.port=9090

Port for SocketIO connector
--socketio.port=8080

### Debugging ###
1. Create "Remote" template in Intellij Idea
2. Run jar with java -jar -Xdebug -Xrunjdwp:transport=dt_socket,server=y,suspend=n,address=5005 build/libs/quickbet-microservice-100-SNAPSHOT.jar --socketio.port=8080 --server.port=9090
