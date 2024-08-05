To Set up this application we need to install and start below stuff

1.> MongoDB
2.> Kafka
3.> Spark cluster

Note : We are using leaderboard MongoDB schema
How to start spark cluster
==========================
Make sure spark is installed in your system and path has set properly.
Then go to command prompt and need to run these 2 commands

# spark-class org.apache.spark.deploy.master.Master
 once you will run above command from cmd then it will start spark cluster
 and along with below ip address this ip may change on certain interval
# spark-class org.apache.spark.deploy.worker.Worker spark://192.168.43.86:7077
 you need to take ip and port from master spark cluster, and you can run this command
 which will registered worker node to master you can also see this registered worker node.
 on master cluster node gui portal http://in01n04804.icepor.com:8080/
 where 8080 is port on where master cluster node is running

#Swagger path
http://localhost:9090/swagger-ui/index.html?configUrl=/api-docs/swagger-config

Available Environment for this MS:
===============================
1.> DEV
2.> TST0
3.> BETA
4.> STRESS
5.> PROD0
