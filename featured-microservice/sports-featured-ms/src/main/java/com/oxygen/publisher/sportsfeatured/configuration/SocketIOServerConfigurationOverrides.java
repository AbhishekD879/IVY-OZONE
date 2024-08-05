package com.oxygen.publisher.sportsfeatured.configuration;

import com.corundumstudio.socketio.SocketIOServer;
import com.corundumstudio.socketio.protocol.JacksonJsonSupport;
import com.corundumstudio.socketio.protocol.JsonSupport;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.oxygen.publisher.context.AbstractSessionContext;
import com.oxygen.publisher.server.SocketIOConnector;
import com.oxygen.publisher.sportsfeatured.model.SportsCachedData;
import com.oxygen.publisher.sportsfeatured.service.FeaturedService;
import com.oxygen.publisher.sportsfeatured.service.SportIdFilter;
import com.oxygen.publisher.sportsfeatured.service.SportsPageIdRegistration;
import io.netty.buffer.ByteBufOutputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.context.annotation.Primary;

@Configuration
public class SocketIOServerConfigurationOverrides {

  @Bean
  public SportsPageIdRegistration sportsPageIdRegistration(
      FeaturedService featuredService,
      SportIdFilter sportIdFilter,
      SportsCachedData sportsCachedData) {

    return new SportsPageIdRegistration(featuredService, sportIdFilter, sportsCachedData);
  }

  @Bean
  @Primary
  public SocketIOConnector featuredSocketIOConnector(
      SocketIOServer socketIoServer, AbstractSessionContext sessionContext) {
    return new SocketIOConnector(socketIoServer, sessionContext);
  }

  @Bean
  @Primary
  public JsonSupport jacksonJsonSupport(ObjectMapper featuredObjectMapper) {
    return new JacksonJsonSupport() {

      @Override
      public void writeValue(ByteBufOutputStream out, Object value) throws IOException {
        byte[] bytes =
            featuredObjectMapper.writeValueAsString(value).getBytes(StandardCharsets.UTF_8);

        out.write(bytes, 0, bytes.length);
        out.flush();
      }
    };
  }
}
