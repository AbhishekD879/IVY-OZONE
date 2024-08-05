package com.entain.oxygen.betbuilder_middleware.config;

import io.netty.channel.EventLoopGroup;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;

@ExtendWith(MockitoExtension.class)
class EventLoopConfigurerTest {

  @Test
  void test() {
    EventLoopGroup group = EventLoopConfigurer.getEventLoopGroup(false, "Any-Thread", 2, 2, 120);
    Assertions.assertNotNull(group);
  }
}
