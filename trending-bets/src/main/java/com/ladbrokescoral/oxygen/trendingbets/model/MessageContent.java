package com.ladbrokescoral.oxygen.trendingbets.model;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Data;
import org.springframework.messaging.Message;
import org.springframework.messaging.MessageHeaders;
import org.springframework.messaging.support.MessageBuilder;

@Data
@AllArgsConstructor
public class MessageContent implements Message<String> {
  String content;

  private static ObjectMapper mapper = new ObjectMapper();

  static {
    mapper.setSerializationInclusion(JsonInclude.Include.NON_NULL);
    mapper.configure(SerializationFeature.FAIL_ON_EMPTY_BEANS, false);
  }

  @Override
  public String getPayload() {
    return content;
  }

  @Override
  public MessageHeaders getHeaders() {
    return new MessageHeaders(new HashMap<>());
  }

  public static Message<String> withPayload(String event, Object... data) {

    StringBuilder builder = new StringBuilder();

    List<Object> dataList = new ArrayList<>();
    dataList.add(event);
    dataList.addAll(Arrays.asList(data));

    try {
      builder.append(mapper.writeValueAsString(dataList));
    } catch (JsonProcessingException e) {
      throw new MessageContentException(e.getMessage());
    }

    return MessageBuilder.withPayload(builder.toString()).build();
  }

  public static Message<String> withInitialPayload(String sid) {

    StringBuilder builder = new StringBuilder();
    InitialMessage msg = new InitialMessage(sid, "25000", "60000");
    try {
      builder.append(mapper.writeValueAsString(msg));
    } catch (JsonProcessingException e) {
      throw new MessageContentException(e.getMessage());
    }

    return MessageBuilder.withPayload(builder.toString()).build();
  }

  @AllArgsConstructor
  @Data
  public static class InitialMessage implements Serializable {

    private String sid;
    private String pingInterval;
    private String pingTimeout;
  }
}
