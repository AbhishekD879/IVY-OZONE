package com.oxygen.publisher.configuration;

import com.corundumstudio.socketio.protocol.JacksonJsonSupport;
import com.corundumstudio.socketio.protocol.JsonSupport;
import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.PropertyAccessor;
import com.fasterxml.jackson.databind.ObjectMapper;
import io.netty.buffer.ByteBufOutputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.http.converter.json.Jackson2ObjectMapperBuilder;

@Configuration
public class JsonSupportConfig {

  @Bean
  public ObjectMapper objectMapper() {
    return new Jackson2ObjectMapperBuilder()
        .visibility(PropertyAccessor.FIELD, JsonAutoDetect.Visibility.ANY)
        .visibility(PropertyAccessor.GETTER, JsonAutoDetect.Visibility.NONE)
        .visibility(PropertyAccessor.SETTER, JsonAutoDetect.Visibility.NONE)
        .visibility(PropertyAccessor.CREATOR, JsonAutoDetect.Visibility.NONE)
        .failOnUnknownProperties(false)
        .failOnEmptyBeans(false)
        .serializationInclusion(JsonInclude.Include.NON_NULL)
        .build();
  }

  @Bean
  public JsonSupport jsonSupport(ObjectMapper objectMapper) {
    return new JacksonJsonSupport() {
      @Override
      public void writeValue(ByteBufOutputStream out, Object value) throws IOException {
        String str = objectMapper.writeValueAsString(value);
        byte[] bytes = str.getBytes(StandardCharsets.UTF_8);
        out.write(bytes, 0, bytes.length);
        out.flush();
        // shouldn't we close the output stream?
      }
    };
  }
}
