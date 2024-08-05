# ToDo: OUTDATED ... !RewriteME! #
# CRLAT WS clients Architecture #

The aim of the project is to design and implement basic event sourcing pattern based on 
[Clean Architecture](https://8thlight.com/blog/uncle-bob/2012/08/13/the-clean-architecture.html) (CA) and [Domain Driven Design](https://en.wikipedia.org/wiki/Domain-driven_design) (DDD)

# Application core state #
Consist of two central circles of CA model, implemented as DDD. 

## Drivers ##
Drivers should handle connection layer to 3rd party services  
Currently they are split to protocol and transport sub-layers. 

## Transports ##
Transports are REQUIRED part of driver. The iam of the transport is to handle communication with outside world, like DB's, web-services.
Each transport should have upstream interface. The upstream object of transport might be Application Interface Adaptors or intermediate Protocols.

## Protocols ##
Protocols introduced as an enveloping Interface Adaptors. For instance socket.io and SockJs supports HTTP polling, web-socket and more transports.
Protocols are designed mostly to for data formatting.