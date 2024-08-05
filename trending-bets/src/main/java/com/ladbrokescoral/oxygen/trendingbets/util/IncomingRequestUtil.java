package com.ladbrokescoral.oxygen.trendingbets.util;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.trendingbets.model.ClientAction;
import com.ladbrokescoral.oxygen.trendingbets.model.IncomingRequest;
import java.util.List;

public class IncomingRequestUtil {
  private static final int TWO = 2;

  private IncomingRequestUtil() {}

  public static IncomingRequest getIncomingRequest(String message) throws JsonProcessingException {
    ClientAction action;
    if (message.length() <= TWO) {
      // Request for ping(2), closeconnection(1,41)
      if (message.equalsIgnoreCase("2")) {
        action = ClientAction.PING;
      } else {
        action = ClientAction.DISCONNECT;
      }
      return new IncomingRequest(action, null);
    }
    List<Object> result = new ObjectMapper().readValue(message, new TypeReference<>() {});

    try {
      action = ClientAction.valueOf(String.valueOf(result.get(0)).toUpperCase());
    } catch (IllegalArgumentException e) {
      action = ClientAction.DEFAULT;
    }

    return new IncomingRequest(action, result.size() > 1 ? result.get(1) : null);
  }
}
