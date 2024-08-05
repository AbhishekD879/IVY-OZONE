package com.ladbrokescoral.oxygen.timeline.api.ws.model;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.List;

public class IncomingRequestUtil {
  private IncomingRequestUtil() {}

  private static final int TWO = 2;

  public static IncomingRequest getIncomingRequest(String message) throws JsonProcessingException {
    if (message.length() <= TWO && message.equalsIgnoreCase("2")) {
      return IncomingRequest.builder().clientAction(ClientAction.PING).build();
    }

    message = message.substring(TWO);
    List<Object> result =
        new ObjectMapper().readValue(message, new TypeReference<List<Object>>() {});

    return IncomingRequest.builder()
        .clientAction(ClientAction.valueOf(String.valueOf(result.get(0)).toUpperCase()))
        .input(result.size() > 1 ? result.get(1) : null)
        .build();
  }
}
