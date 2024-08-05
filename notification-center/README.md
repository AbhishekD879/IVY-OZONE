**Getting started**

Requirements:

* gradle version [2.5 ... 3.5]
* java version 1.8
* docker version > 18
* docker-compose version 1.18.0


1. Clone project:

     **git clone git@bitbucket.org:symphonydevelopers/notification-center.git**
 
2. Navigate to project:
 
    **cd notification-center**
    
3. Start redis:

    **docker-compose up -d**
    
4. Build application:

    **bash ./gradlew**
    
5. Run application:

    **java -jar build/libs/notification-center-86.0.0.jar**
    
6. Register device and event:

    **cd http/**
    
    For android devices:
    
    **curl -X PUT http://localhost:8080/subscribe -H "Content-Type: application/json" -d @android.json**
    
    For apple devices:
    
    **curl -X PUT http://localhost:8080/subscribe -H "Content-Type: application/json" -d @apple.json**
