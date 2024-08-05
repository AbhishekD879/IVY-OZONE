package com.ladbrokescoral.oxygen.timeline.api.reactive.model;

import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.ladbrokescoral.oxygen.timeline.api.exceptions.MessageContentException;
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
import org.springframework.web.reactive.socket.WebSocketSession;

@Data
@AllArgsConstructor
public class MessageContent implements Message<String> {
  String content;

  private static ObjectMapper mapper;
  private static final int TWO = 2;
  private static final int FOUR = 4;
  private static final int EMPTY_PAYLOAD_CODE = 40;
  private static final long PING_INTERVAL = 25000;
  private static final long PING_TIMEOUT = 60000;

  static {
    mapper =
        new ObjectMapper()
            .registerModule(new JavaTimeModule())
            .setSerializationInclusion(JsonInclude.Include.NON_NULL)
            .disable(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS);
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
    builder.append(FOUR);
    builder.append(TWO);

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

  public static Message<String> withInitialPayload(WebSocketSession session) {

    StringBuilder builder = new StringBuilder();
    builder.append(0);
    InitialMessage msg =
        new InitialMessage(
            session.getId(), PING_INTERVAL, PING_TIMEOUT, new String[] {"websocket"});
    try {
      builder.append(mapper.writeValueAsString(msg));
    } catch (JsonProcessingException e) {
      throw new MessageContentException(e.getMessage());
    }

    return MessageBuilder.withPayload(builder.toString()).build();
  }

  public static Message<String> emptyPayloadToClient() {
    return MessageBuilder.withPayload(String.valueOf(EMPTY_PAYLOAD_CODE)).build();
  }

  @AllArgsConstructor
  @Data
  public static class InitialMessage implements Serializable {
    private String sid;
    private long pingInterval;
    private long pingTimeout;
    private String[] upgrades;
  }
}
