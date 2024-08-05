package com.oxygen.publisher.configuration;

import com.corundumstudio.socketio.SocketIOServer;
import com.oxygen.publisher.context.AbstractSessionContext;
import com.oxygen.publisher.server.SocketIOConnector;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/** Created by Aliaksei Yarotski on 12/26/17. */
@Configuration
public class SocketIOConnectorConfiguration {

  @Bean
  public SocketIOConnector socketIOConnector(
      SocketIOServer socketIoServer, AbstractSessionContext sessionContext) {
    return new SocketIOConnector(socketIoServer, sessionContext);
  }
}
