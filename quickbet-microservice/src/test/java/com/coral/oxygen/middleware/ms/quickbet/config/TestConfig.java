package com.coral.oxygen.middleware.ms.quickbet.config;

import com.coral.oxygen.middleware.ms.quickbet.impl.OnceExecutor;
import com.coral.oxygen.middleware.ms.quickbet.utils.WebSocketTestClient;
import org.springframework.boot.test.context.TestConfiguration;
import org.springframework.context.annotation.Bean;

@TestConfiguration
public class TestConfig {

  @Bean
  public WebSocketTestClient webSocketTestClient() {
    return new WebSocketTestClient();
  }

  @Bean
  public OnceExecutor onceExecutor() {
    return (identity, action, rejectedAction, period) -> action.run();
  }
}
