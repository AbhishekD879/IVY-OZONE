Timeform application
===================
This app consumes data from Timeform data provider and provides as REST API. Also interacts with OpenBet&Siteserv.

# Hazelcast
### Consul configuration
##### Environment properties
We use third-party library for discovering hazelcast nodes [hazelcast-consul-discovery-spi](https://github.com/bitsofinfo/hazelcast-consul-discovery-spi) . This lib provides specific environment properties.

 Parameter                                            | Default value | Comment
 ---------------------------------------------------- |:-------------:| ------:
 consul-host.consul-host                              | localhost     |        
 consul-port.consul-port                              | 8500          |        
 consul-healthy-only.consul-healthy-only | true       |               |        
 consul-discovery-delay-ms.consul-discovery-delay-ms  | 10000         |        

More information about consul parameters we can find in [hazelcast-tst2.xml](src/main/resources/hazelcast-tst2.xml) configuration file.

So We can pass custom consul host/port to application using the following command :

		java  -jar build/libs/timeform.jar -Dconsul-host.consul-host={your host} -Dconsul-port.consul-port=8501
 



