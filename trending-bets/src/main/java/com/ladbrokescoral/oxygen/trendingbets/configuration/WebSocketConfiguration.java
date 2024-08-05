package com.ladbrokescoral.oxygen.trendingbets.configuration;

import java.util.HashMap;
import java.util.Map;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.web.reactive.handler.SimpleUrlHandlerMapping;
import org.springframework.web.reactive.socket.WebSocketHandler;
import org.springframework.web.reactive.socket.server.WebSocketService;
import org.springframework.web.reactive.socket.server.support.HandshakeWebSocketService;
import org.springframework.web.reactive.socket.server.support.WebSocketHandlerAdapter;
import org.springframework.web.reactive.socket.server.upgrade.ReactorNettyRequestUpgradeStrategy;
import reactor.netty.http.server.WebsocketServerSpec;

@Configuration
public class WebSocketConfiguration {

  @Bean
  public SimpleUrlHandlerMapping handlerMapping(WebSocketHandler handler) {
    Map<String, WebSocketHandler> map = new HashMap<>();
    map.put("/trendingbets", handler);
    SimpleUrlHandlerMapping mapping = new SimpleUrlHandlerMapping();
    mapping.setUrlMap(map);
    return mapping;
  }

  @Bean
  public WebSocketHandlerAdapter handlerAdapter() {
    return new WebSocketHandlerAdapter(webSocketService());
  }

  @Bean
  public WebSocketService webSocketService() {
    return new HandshakeWebSocketService(
        new ReactorNettyRequestUpgradeStrategy(
            WebsocketServerSpec.builder().compress(true).handlePing(true)));
  }
}
